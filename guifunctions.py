import flask
from PySide2 import QtGui
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from ecdsa import SigningKey
from db import createUser, addKey, getUserKeyPair


class UserCreationWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self,app):
        super().__init__()
        self.setWindowTitle("Create a user")
        layout = QVBoxLayout()
        self.resize(400,200)
        self.app = app
        self.usernamefield = QLineEdit()
        self.usernamefield.setText("Username")
        self.passwordfield = QLineEdit()
        self.passwordfield.setText("Password")
        self.submitbutton = QPushButton()
        self.submitbutton.clicked.connect(lambda : self.action())
        self.submitbutton.setText("Create User")
        self.passwordfield.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.usernamefield)
        layout.addWidget(self.passwordfield)
        layout.addWidget(self.submitbutton)
        self.setLayout(layout)
    def action(self):
        sk = SigningKey.generate()
        vk = sk.get_verifying_key()
        with self.app.app_context():
            user = createUser(self.usernamefield.text(), vk.to_string().hex())
            print(addKey(user['user'],sk.to_string(), self.passwordfield.text()))
            print(getUserKeyPair(user['user'],self.passwordfield.text()))
        self.close()