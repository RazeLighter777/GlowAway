from PySide2 import QtGui
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel


class UserCreationWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.resize(200,200)
        self.label = QLabel("User Creation")
        layout.addWidget(self.label)