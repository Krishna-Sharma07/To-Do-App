from PySide6.QtWidgets import QWidget, QListWidget, QLabel, QVBoxLayout, QHBoxLayout

class Main_Widget(QWidget):
    def __init__(self):
        super().__init__()
        task_list_lable = QLabel("Task Lists")
        list_of_lists = QListWidget()
        list_of_lists.resize(300, 1000)

        task_list_layout = QVBoxLayout()
        task_list_layout.addWidget(task_list_lable)
        task_list_layout.addWidget(list_of_lists)


        tasks_widget = QListWidget()
        tasks_widget.resize(700, 1000)

        layout = QHBoxLayout()
        layout.addLayout(task_list_layout)
        layout.addWidget(tasks_widget)

        self.setLayout(layout)