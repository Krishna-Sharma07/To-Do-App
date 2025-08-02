from PySide6.QtWidgets import QMainWindow, QSizePolicy, QToolBar ,QWidget, QPushButton, QMessageBox, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog, QFileDialog, QListWidgetItem
import json
from PySide6.QtCore import Qt

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
        self.task_states = {}

        self.setLayout(layout)

    def add_list(self, list_name):
        if list_name and not any(self.list_of_lists.item(i).text() == list_name for i in range(self.list_of_lists.count())):
            self.tasks_by_list[list_name] = []
            self.list_of_lists.addItem(list_name)


    def add_task(self, task):
        current_list = self.list_of_lists.currentItem().text()
        if current_list:
            self.tasks_by_list[current_list].append(task)
            self.display()

    def display(self):
        self.tasks_widget.clear()
        current_item = self.list_of_lists.currentItem()
        if not current_item:
            return
        list_name = current_item.text()

        for task_text in self.tasks_by_list[list_name]:
            if task_text not in self.task_states:
                self.task_states[task_text] = {"completed": False}

            if self.current_filter == "Completed" and not self.task_states[task_text]["completed"]:
                continue
            if self.current_filter == "Pending" and self.task_states[task_text]["completed"]:
                continue

            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if self.task_states[task_text]["completed"] else Qt.Unchecked)
            self.tasks_widget.addItem(item)

    def get_data(self):
        return {
            "tasks": self.tasks_by_list,
            "states": self.task_states
        }

    def load_data(self, data):
        self.tasks_by_list = data.get("tasks", {})
        self.task_states = data.get("states", {})
        self.list_of_lists.clear()
        self.tasks_widget.clear()
        for list_name in self.tasks_by_list:
            self.list_of_lists.addItem(list_name)

    def toggle_task_status(self, item):
        task_text = item.text()
        self.task_states[task_text] = {"completed": (item.checkState() == Qt.Checked)}

    def set_filter(self, filter_type):
        self.current_filter = filter_type
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
        due_date = task_menu.addAction("Set Due Date")
        reminder = task_menu.addAction("Set Reminder")
        repeat_task = task_menu.addAction("Repeat Task")

        view_menu = menu_bar.addMenu("&View")
        all_task = view_menu.addAction("All Tasks")
        all_task.triggered.connect(lambda: self.centralWidget().set_filter("All"))
        completed = view_menu.addAction("Completed Tasks")
        completed.triggered.connect(lambda: self.centralWidget().set_filter("Completed"))
        pending = view_menu.addAction("Pending Tasks")
        pending.triggered.connect(lambda: self.centralWidget().set_filter("Pending"))
        overdue = view_menu.addAction("Overdue Tasks")
        sort_by = view_menu.addAction("Sort by")
        filter_by = view_menu.addAction("Filter by")
        dark_mode = view_menu.addAction("Dark Mode")

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        add_task = QPushButton("+ Add Task")
        add_task.clicked.connect(self.add_task_func)
        search_task_lable = QLabel("        Search Task:   ")
        search_task = QLineEdit()

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

    def mark_incomplete(self):
        task_widget = self.centralWidget().tasks_widget
        item = task_widget.currentItem()
        if item:
            item.setCheckState(Qt.Unchecked)

    

