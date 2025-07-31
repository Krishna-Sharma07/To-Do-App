from PySide6.QtWidgets import QMainWindow, QSizePolicy, QToolBar ,QWidget, QMessageBox, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog

class Main_Widget(QWidget):
    def __init__(self):

        super().__init__()

        task_list_lable = QLabel("Task Lists")

        self.list_of_lists = QListWidget(self)
        self.list_of_lists.setMinimumSize(300, 1000)
        self.list_of_lists.setMaximumSize(700, 2000)

        task_list_layout = QVBoxLayout()
        task_list_layout.addWidget(task_list_lable)
        task_list_layout.addWidget(self.list_of_lists)

        self.tasks_widget = QListWidget()
        self.tasks_widget.setMinimumSize(700, 1000)
        self.tasks_widget.setMaximumSize(2000, 2000)

        layout = QHBoxLayout()
        layout.addLayout(task_list_layout)
        layout.addWidget(self.tasks_widget)

        self.setLayout(layout)

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
        save_as = file_menu.addAction("Save As")
        exit_app = file_menu.addAction("Exit")

        edit_menu = menu_bar.addMenu("&Edit")
        undo = edit_menu.addAction("Undo")
        redo = edit_menu.addAction("Redo")
        cut = edit_menu.addAction("Cut")
        copy = edit_menu.addAction("Copy")
        paste = edit_menu.addAction("Paste")
        delete_task = edit_menu.addAction("Delete Task")
        edit_task = edit_menu.addAction("Edit Task")

        task_menu = menu_bar.addMenu("&Task")
        complete = task_menu.addAction("Mark Complete")
        incomplete = task_menu.addAction("Mark Incomplete")
        priority = task_menu.addAction("Set Priority")
        due_date = task_menu.addAction("Set Due Date")
        reminder = task_menu.addAction("Set Reminder")
        repeat_task = task_menu.addAction("Repeat Task")

        view_menu = menu_bar.addMenu("&View")
        all_task = view_menu.addAction("All Tasks")
        completed = view_menu.addAction("Completed Tasks")
        pending = view_menu.addAction("Pending Tasks")
        overdue = view_menu.addAction("Overdue Tasks")
        sort_by = view_menu.addAction("Sort by")
        filter_by = view_menu.addAction("Filter by")
        dark_mode = view_menu.addAction("Dark Mode")

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        add_task = QPushButton("+ Add Task")
        search_task_lable = QLabel("        Search Task:   ")
        search_task = QLineEdit()

        tool_bar.addWidget(add_task)
        tool_bar.addSeparator()
        tool_bar.addWidget(search_task_lable)
        tool_bar.addWidget(search_task)

        main_widget = Main_Widget()

        self.setCentralWidget(main_widget)

    def add_task_func(self):
        text, ok = QInputDialog.getText(self, "Add New Task", "Enter Task name:")
        if ok and text:
            self.centralWidget().tasks_widget.addItem(text)

    def add_list_func(self):
        text, ok = QInputDialog.getText(self, "Add New List", "Enter List name:")
        if ok and text:
            self.centralWidget().list_of_lists.addItem(text)
