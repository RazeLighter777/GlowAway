import flask
from PySide2 import QtGui
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from ecdsa import SigningKey
from db import createUser, addKey, getUserKeyPair, getUsersWithKeys, getAliasesWithUUIDs, getUserAlias, \
    createFingerprint


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
        self.passwordfield = QLineEdit()
        self.usernamefield.setPlaceholderText("Username")
        self.passwordfield.setPlaceholderText("Password")
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
        self.close()

class UserSelectionWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self,app,label):
        super().__init__()
        self.extlabel = label
        self.setWindowTitle("Select the current user")
        layout = QVBoxLayout()
        self.resize(400,200)
        self.app = app
        self.submitbutton = QPushButton()
        self.passwordfield = QLineEdit()
        self.passwordfield.setPlaceholderText("Password")
        self.passwordfield.setEchoMode(QLineEdit.EchoMode.Password)
        self.label = QLabel()
        self.label.setText("Select the user you wish to login as and enter their password: ")
        self.submitbutton.clicked.connect(lambda : self.action())
        self.passwordfield.returnPressed.connect(lambda : self.action())
        self.submitbutton.setText("Select User")
        self.userSelection = QComboBox()
        with self.app.app_context():
            self.uuids = getUsersWithKeys()
            self.userSelection.addItems(getAliasesWithUUIDs(self.uuids))
        self.setLayout(layout)
        layout.addWidget(self.label)
        layout.addWidget(self.userSelection)
        layout.addWidget(self.passwordfield)
        layout.addWidget(self.submitbutton)

    def action(self):
        with self.app.app_context():
            self.app.currentUser = self.uuids[self.userSelection.currentIndex()]
            keys =  getUserKeyPair(self.app.currentUser, self.passwordfield.text())
            if "error" in keys:
                self.label.setText("Error: Password incorrect")
                return
            self.app.currentUserKeys = keys
            self.extlabel.setText("Logged in as: " + getUserAlias(self.app.currentUser) + " with ID " + self.app.currentUser)

        self.close()

