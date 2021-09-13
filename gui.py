from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from guifunctions import UserCreationWindow


class MainGui(object):
    def setupUi(self, dd):
        if not dd.objectName():
            dd.setObjectName(u"dd")
        dd.resize(967, 527)
        self.actionAdd_router = QAction(dd)
        self.actionAdd_router.setObjectName(u"actionAdd_router")
        self.actionHelp = QAction(dd)
        self.actionHelp.setObjectName(u"actionHelp")
        self.actionAbout_GlowAway = QAction(dd)
        self.actionAbout_GlowAway.setObjectName(u"actionAbout_GlowAway")
        self.actionUser_Settings = QAction(dd)
        self.actionUser_Settings.setObjectName(u"actionUser_Settings")
        self.actionCreate_User = QAction(dd)
        self.actionUser_Settings.setObjectName(u"actionCreate_Uesr")

        self.actionAdd_Room = QAction(dd)
        self.actionAdd_Room.setObjectName(u"actionAdd_Room")
        self.actionAdd_router_2 = QAction(dd)
        self.actionAdd_router_2.setObjectName(u"actionAdd_router_2")
        self.actionAdd_room = QAction(dd)
        self.actionAdd_room.setObjectName(u"actionAdd_room")
        self.actionPrivate_message = QAction(dd)
        self.actionPrivate_message.setObjectName(u"actionPrivate_message")
        self.centralwidget = QWidget(dd)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout.addWidget(self.listView)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout.addWidget(self.textBrowser)

        self.horizontalLayout.setStretch(1, 5)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        font = QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 30))
        self.pushButton.setFont(font)

        self.verticalLayout_2.addWidget(self.pushButton)

        dd.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(dd)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 967, 29))
        self.menuConnect = QMenu(self.menubar)
        self.menuConnect.setObjectName(u"menuConnect")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuNetwork = QMenu(self.menubar)
        self.menuNetwork.setObjectName(u"menuNetwork")
        dd.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(dd)
        self.statusbar.setObjectName(u"statusbar")
        dd.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuNetwork.menuAction())
        self.menubar.addAction(self.menuConnect.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuConnect.addAction(self.actionUser_Settings)
        self.menuConnect.addAction(self.actionCreate_User)
        self.menuConnect.addAction(self.actionAdd_Room)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionHelp)
        self.menuAbout.addAction(self.actionAbout_GlowAway)
        self.menuNetwork.addAction(self.actionAdd_router_2)
        self.menuNetwork.addAction(self.actionAdd_room)
        self.menuNetwork.addAction(self.actionPrivate_message)

        self.retranslateUi(dd)

        QMetaObject.connectSlotsByName(dd)

    # setupUi

    def retranslateUi(self, dd):
        dd.setWindowTitle(QCoreApplication.translate("dd", u"MainWindow", None))
        self.actionAdd_router.setText(QCoreApplication.translate("dd", u"Add router", None))
        self.actionHelp.setText(QCoreApplication.translate("dd", u"Help", None))
        self.actionAbout_GlowAway.setText(QCoreApplication.translate("dd", u"About GlowAway", None))
        self.actionUser_Settings.setText(QCoreApplication.translate("dd", u"User Settings", None))
        self.actionCreate_User.setText(QCoreApplication.translate("dd", u"Create User", None))
        self.actionAdd_Room.setText(QCoreApplication.translate("dd", u"Network Settings", None))
        self.actionAdd_router_2.setText(QCoreApplication.translate("dd", u"Add router", None))
        self.actionAdd_room.setText(QCoreApplication.translate("dd", u"Add room", None))
        self.actionPrivate_message.setText(QCoreApplication.translate("dd", u"Private message", None))
        # if QT_CONFIG(tooltip)
        self.listView.setToolTip(
            QCoreApplication.translate("dd", u"<html><head/><body><p>List of Rooms</p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.textBrowser.setDocumentTitle(QCoreApplication.translate("dd", u"Chat", None))
        self.pushButton.setText(QCoreApplication.translate("dd", u"PushButton", None))
        self.menuConnect.setTitle(QCoreApplication.translate("dd", u"Settings", None))
        self.menuAbout.setTitle(QCoreApplication.translate("dd", u"About", None))
        self.menuNetwork.setTitle(QCoreApplication.translate("dd", u"Chat", None))
    # retranslateUi


class MainWindow(QMainWindow, MainGui):

    #

    def __init__(self):
        #

        QMainWindow.__init__(self)

        #

        self.setupUi(self)

        self.connectMe()
        self.dialogs = []
        #

        self.setWindowTitle("GlowAway")

    #

    def connectMe(self):
        self.pushButton.clicked.connect(lambda: self.textBrowser.insertPlainText(self.lineEdit.text() + "\n"))
        self.actionCreate_User.triggered.connect(lambda: self.showUserCreation())

    def showUserCreation(self):
        print("Showing")
        w = UserCreationWindow()
        self.dialogs.append(w)
        print(self.dialogs)
        w.show()

    #

    def slotButton(self):
        self.label.setText("GlowAway")
