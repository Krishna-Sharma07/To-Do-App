from PySide6.QtWidgets import QApplication
import sys
from to_do_app import Window

app = QApplication(sys.argv)

window = Window(app)
window.show()

app.exec()
