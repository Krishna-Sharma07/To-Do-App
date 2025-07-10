from PySide6.QtWidgets import QMainWindow, QSizePolicy, QToolBar ,QWidget, QMessageBox, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QListWidget
from PySide6.QtGui import QAction
from main_widget import Main_Widget

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
        new_list = file_menu.addAction("New List")
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