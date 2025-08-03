from PySide6.QtWidgets import (QMainWindow, QSizePolicy, QToolBar ,QWidget, QPushButton, 
                            QMessageBox, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, 
                            QListWidget, QInputDialog, QFileDialog, QListWidgetItem, 
                            QDateEdit, QDialog, QTimeEdit)
import json
from PySide6.QtCore import Qt, QDate, QTime
from datetime import datetime

class Main_Widget(QWidget):
    def __init__(self):

        super().__init__()
        self.tasks_by_list = {}

        task_list_lable = QLabel("Task Lists")

        self.list_of_lists = QListWidget(self)
        self.list_of_lists.setMinimumSize(300, 1000)
        self.list_of_lists.setMaximumSize(700, 2000)

        self.list_of_lists.currentItemChanged.connect(self.display)

        task_list_layout = QVBoxLayout()
        task_list_layout.addWidget(task_list_lable)
        task_list_layout.addWidget(self.list_of_lists)

        self.tasks_widget = QListWidget()
        self.tasks_widget.itemChanged.connect(self.toggle_task_status)
        self.tasks_widget.setMinimumSize(700, 1000)
        self.tasks_widget.setMaximumSize(2000, 2000)

        layout = QHBoxLayout()
        layout.addLayout(task_list_layout)
        layout.addWidget(self.tasks_widget)

        self.current_filter = "All"

        self.setLayout(layout)

    def add_list(self, list_name):
        if list_name and not any(self.list_of_lists.item(i).text() == list_name for i in range(self.list_of_lists.count())):
            self.tasks_by_list[list_name] = []
            self.list_of_lists.addItem(list_name)



    def add_task(self, task_text):
        current_list_item = self.list_of_lists.currentItem()
        if current_list_item:
            list_name = current_list_item.text()
            task_data = {
                "text": task_text,
                "completed": False,
                "priority": "Low", 
                "due": None, 
                "reminder": None
            }
            self.tasks_by_list[list_name].append(task_data)
            self.display()


    def display(self):
        self.tasks_widget.clear()
        current_item = self.list_of_lists.currentItem()
        if not current_item:
            return
        list_name = current_item.text()

        for task in self.tasks_by_list[list_name]:
            if self.current_filter == "Completed" and not task["completed"]:
                continue
            if self.current_filter == "Pending" and task["completed"]:
                continue
            if self.current_filter == "Overdue":
                if not task["due"]:
                    continue
                try:
                    due_date = datetime.strptime(task["due"], "%Y-%m-%d").date()
                    if due_date >= datetime.today().date() or task["completed"]:
                        continue
                except ValueError:
                    continue 

            display_text = task["text"]

            if task["priority"] == "High":
                display_text = "★ " + display_text
            elif task["priority"] == "Medium":
                display_text = "☆ " + display_text  

            extras = []
            if task["due"]:
                extras.append(f"Due: {task['due']}")
            if task["reminder"]:
                extras.append(f"Remind: {task['reminder']}")

            if extras:
                display_text += "  (" + ", ".join(extras) + ")"

            item = QListWidgetItem(display_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if task["completed"] else Qt.Unchecked)
            self.tasks_widget.addItem(item)

    def get_data(self):
        return self.tasks_by_list


    def load_data(self, data):
        self.tasks_by_list = data
        self.list_of_lists.clear()
        self.tasks_widget.clear()
        for list_name in self.tasks_by_list:
            self.list_of_lists.addItem(list_name)

    def toggle_task_status(self, item):
        current_list_item = self.list_of_lists.currentItem()
        if current_list_item:
            list_name = current_list_item.text()

            base_text = item.text().replace("★ ", "").replace("☆ ", "").split("  (")[0]

            for task in self.tasks_by_list[list_name]:
                if task["text"] == base_text:
                    task["completed"] = (item.checkState() == Qt.Checked)
                    break


    def set_filter(self, filter_type):
        self.current_filter = filter_type
        self.display()

    def set_priority(self):
        current_list_item = self.list_of_lists.currentItem()
        task_item = self.tasks_widget.currentItem()

        if current_list_item and task_item:
            list_name = current_list_item.text()
            base_text = task_item.text().replace("★ ", "").replace("☆ ", "").split("  (")[0]

            priorities = ["High", "Medium", "Low"]
            priority, ok = QInputDialog.getItem(self, "Set Priority", "Select priority:", priorities, 2, False)

            if ok:
                for task in self.tasks_by_list[list_name]:
                    if task["text"] == base_text:
                        task["priority"] = priority
                        break
                self.display()

    def set_due_date(self):
        current_list_item = self.list_of_lists.currentItem()
        task_item = self.tasks_widget.currentItem()

        if current_list_item and task_item:
            list_name = current_list_item.text()
            base_text = task_item.text().replace("★ ", "").replace("☆ ", "").split("  (")[0]

            date_dialog = QDialog(self)
            date_dialog.setWindowTitle("Set Due Date")
            layout = QVBoxLayout()

            label = QLabel("Select Due Date:")
            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDate(QDate.currentDate())

            save_btn = QPushButton("Set Due Date")
            save_btn.clicked.connect(date_dialog.accept)

            layout.addWidget(label)
            layout.addWidget(date_edit)
            layout.addWidget(save_btn)
            date_dialog.setLayout(layout)

            if date_dialog.exec():
                due_date_str = date_edit.date().toString("yyyy-MM-dd")
                for task in self.tasks_by_list[list_name]:
                    if task["text"] == base_text:
                        task["due"] = due_date_str
                        break
                self.display()

    def set_reminder(self):
        current_list_item = self.list_of_lists.currentItem()
        task_item = self.tasks_widget.currentItem()

        if current_list_item and task_item:
            list_name = current_list_item.text()
            base_text = task_item.text().replace("★ ", "").replace("☆ ", "").split("  (")[0]

            reminder_dialog = QDialog(self)
            reminder_dialog.setWindowTitle("Set Reminder")
            layout = QVBoxLayout()

            date_label = QLabel("Select Reminder Date:")
            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDate(QDate.currentDate())

            time_label = QLabel("Select Reminder Time:")
            time_edit = QTimeEdit()
            time_edit.setTime(QTime.currentTime())

            save_btn = QPushButton("Set Reminder")
            save_btn.clicked.connect(reminder_dialog.accept)

            layout.addWidget(date_label)
            layout.addWidget(date_edit)
            layout.addWidget(time_label)
            layout.addWidget(time_edit)
            layout.addWidget(save_btn)
            reminder_dialog.setLayout(layout)

            if reminder_dialog.exec():
                reminder_str = f"{date_edit.date().toString('yyyy-MM-dd')} {time_edit.time().toString('HH:mm')}"
                for task in self.tasks_by_list[list_name]:
                    if task["text"] == base_text:
                        task["reminder"] = reminder_str
                        break
                self.display()
    
    def sort_tasks(self, sort_type):
        current_list_item = self.list_of_lists.currentItem()
        if not current_list_item:
            return
        list_name = current_list_item.text()

        if sort_type == "Name":
            self.tasks_by_list[list_name].sort(key=lambda x: x["text"].lower())

        elif sort_type == "Due Date":
            from datetime import datetime
            self.tasks_by_list[list_name].sort(
                key=lambda x: datetime.strptime(x["due"], "%Y-%m-%d") if x["due"] else datetime.max
            )

        elif sort_type == "Priority":
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            self.tasks_by_list[list_name].sort(
                key=lambda x: priority_order.get(x["priority"], 4)
            )

        elif sort_type == "Completion":
            self.tasks_by_list[list_name].sort(key=lambda x: x["completed"])

        self.display()



class Window(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.resize(1000,1000)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWindowTitle("To Do App")

        menu_bar = self.menuBar()

        file_menu =  menu_bar.addMenu("&File")
        new_task = file_menu.addAction("New Task")
        new_task.triggered.connect(self.add_task_func)
        new_list = file_menu.addAction("New List")
        new_list.triggered.connect(self.add_list_func)
        save = file_menu.addAction("Save")
        save.triggered.connect(self.save_to_file)
        load = file_menu.addAction("Load")
        load.triggered.connect(self.load_from_file)
        exit_app = file_menu.addAction("Exit")
        exit_app.triggered.connect(lambda: self.app.quit())

        edit_menu = menu_bar.addMenu("&Edit")
        undo = edit_menu.addAction("Undo")
        redo = edit_menu.addAction("Redo")
        cut = edit_menu.addAction("Cut")
        copy = edit_menu.addAction("Copy")
        paste = edit_menu.addAction("Paste")
        delete_task = edit_menu.addAction("Delete Task")
        edit_task = edit_menu.addAction("Edit Task")
        delete_list = edit_menu.addAction("Delete List")
        edit_list = edit_menu.addAction("Edit List")

        task_menu = menu_bar.addMenu("&Task")
        complete = task_menu.addAction("Mark Complete")
        complete.triggered.connect(self.mark_complete)
        incomplete = task_menu.addAction("Mark Incomplete")
        incomplete.triggered.connect(self.mark_incomplete)
        priority = task_menu.addAction("Set Priority")
        priority.triggered.connect(lambda: self.centralWidget().set_priority())
        due_date = task_menu.addAction("Set Due Date")
        due_date.triggered.connect(lambda: self.centralWidget().set_due_date())
        reminder = task_menu.addAction("Set Reminder")
        reminder.triggered.connect(lambda: self.centralWidget().set_reminder())

        view_menu = menu_bar.addMenu("&View")
        all_task = view_menu.addAction("All Tasks")
        all_task.triggered.connect(lambda: self.centralWidget().set_filter("All"))
        completed = view_menu.addAction("Completed Tasks")
        completed.triggered.connect(lambda: self.centralWidget().set_filter("Completed"))
        pending = view_menu.addAction("Pending Tasks")
        pending.triggered.connect(lambda: self.centralWidget().set_filter("Pending"))
        overdue = view_menu.addAction("Overdue Tasks")
        overdue.triggered.connect(lambda: self.centralWidget().set_filter("Overdue"))
        sort_menu = view_menu.addMenu("Sort by")
        sort_name = sort_menu.addAction("Name (A-Z)")
        sort_due = sort_menu.addAction("Due Date (Earliest First)")
        sort_priority = sort_menu.addAction("Priority (High -> Low)")
        sort_completion = sort_menu.addAction("Completion Status")
        sort_name.triggered.connect(lambda: self.centralWidget().sort_tasks("Name"))
        sort_due.triggered.connect(lambda: self.centralWidget().sort_tasks("Due Date"))
        sort_priority.triggered.connect(lambda: self.centralWidget().sort_tasks("Priority"))
        sort_completion.triggered.connect(lambda: self.centralWidget().sort_tasks("Completion"))

        dark_mode = view_menu.addAction("Dark Mode")
        self.dark_mode_enabled = False
        dark_mode.triggered.connect(self.toggle_dark_mode)

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        add_list = QPushButton("+ Add List")
        add_list.clicked.connect(self.add_list_func)
        add_task = QPushButton("+ Add Task")
        add_task.clicked.connect(self.add_task_func)
        search_task_lable = QLabel("        Search Task:   ")
        search_task = QLineEdit()

        tool_bar.addWidget(add_list)
        tool_bar.addWidget(add_task)
        tool_bar.addSeparator()
        tool_bar.addWidget(search_task_lable)
        tool_bar.addWidget(search_task)

        main_widget = Main_Widget()

        self.setCentralWidget(main_widget)

    def add_task_func(self):
        try:
            current_item = self.centralWidget().list_of_lists.currentItem()
            if not current_item:
                raise ValueError("No list selected. Please create or select a task list first.")

            text, ok = QInputDialog.getText(self, "New Task", "Enter task:")
            if ok and text:
                self.centralWidget().add_task(text)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_list_func(self):
        text, ok = QInputDialog.getText(self, "Add New List", "Enter List name:")
        if ok and text:
            self.centralWidget().add_list(text)

    def save_to_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Task Lists", "", "JSON Files (*.json)")
        if filename:
            try:
                data = self.centralWidget().get_data()
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
                QMessageBox.information(self, "Success", "Task lists saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Save Failed", str(e))

    def load_from_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Task Lists", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                self.centralWidget().load_data(data)
                QMessageBox.information(self, "Success", "Task lists loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Load Failed", str(e))


    def mark_complete(self):
        task_widget = self.centralWidget().tasks_widget
        item = task_widget.currentItem()
        if item:
            item.setCheckState(Qt.Checked)
            self.centralWidget().toggle_task_status(item)

    def mark_incomplete(self):
        task_widget = self.centralWidget().tasks_widget
        item = task_widget.currentItem()
        if item:
            item.setCheckState(Qt.Unchecked)
            self.centralWidget().toggle_task_status(item)


    def toggle_dark_mode(self):
        if self.dark_mode_enabled:
            self.setStyleSheet("")
            self.dark_mode_enabled = False
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                    color: white;
                }
                QWidget {
                    background-color: #121212;
                    color: white;
                }
                QPushButton {
                    background-color: #1E1E1E;
                    color: white;
                    border: 1px solid #333;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
                QLineEdit {
                    background-color: #1E1E1E;
                    color: white;
                    border: 1px solid #333;
                }
                QListWidget {
                    background-color: #1E1E1E;
                    color: white;
                    border: 1px solid #333;
                }
                QMenuBar {
                    background-color: #1E1E1E;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #333;
                }
                QMenu {
                    background-color: #1E1E1E;
                    color: white;
                }
                QMenu::item:selected {
                    background-color: #333;
                }
            """)
            self.dark_mode_enabled = True
