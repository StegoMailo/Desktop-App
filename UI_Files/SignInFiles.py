import re
import threading

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QStackedWidget, QLabel, QFileDialog, QLineEdit
from PyQt5.uic import loadUi

from Authentication.ReadQR import decodeQR
from Gmail import AuthenticateEmail
from Gmail.AuthenticateEmail import authenticateUser


class EmailSignIn(QDialog):
    widgets: QStackedWidget

    def __init__(self, allWidgets):
        super(EmailSignIn, self).__init__()
        loadUi('Email Sign In.ui', self)

        self.widgets = allWidgets.widgets
        self.allWidgets = allWidgets

        self.btnGmail.clicked.connect(self.LogInToGmail)
        self.btnNext.clicked.connect(self.goToQR)

        self.btnHome.clicked.connect(self.cancelSignIn)

    def cancelSignIn(self):
        AuthenticateEmail.authenticated = True
        self.allWidgets.abandonSignIn()

    def LogInToGmail(self):
        self.startTheThread()

    def goToQR(self):
        AuthenticateEmail.authenticated = True
        self.widgets.setCurrentIndex(2)

    def startTheThread(self):
        t = threading.Thread(daemon=True, name='AuthenticationFlow', target=openGmail, args=[self.updateUI])
        t.start()

    def updateUI(self):
        if AuthenticateEmail.currentEmail != "":
            self.txtLoggedEmail.setText("Welcome\n" + AuthenticateEmail.currentEmail)


class Communicate(QObject):
    myGUI_signal = pyqtSignal()


def openGmail(callbackFunc):
    mySrc = Communicate()
    mySrc.myGUI_signal.connect(callbackFunc)
    authenticateUser()

    while not AuthenticateEmail.authenticated:
        continue
    mySrc.myGUI_signal.emit()


class QRSignIn(QDialog):
    widgets: QStackedWidget
    QRFilePath: str

    def __init__(self, allWidgets):
        super(QRSignIn, self).__init__()
        loadUi('QR Sign In.ui', self)

        self.widgets = allWidgets.widgets
        self.allWidgets = allWidgets

        self.txtQR = DraggableFilesQLabelQR(self, self)

        self.txtQR.setStyleSheet(
            "background-color: rgba(138, 198, 253,0.5);   border-radius:10px; border: 0.5px solid #000000;"
            " color: rgb(0,0,0);")

        self.txtQR.setGeometry(140, 280, 251, 221)
        self.txtQR.setText("Drop Your\nQR Code Here")

        tempFont = self.txtQR.font()
        tempFont.setBold(False)
        tempFont.setPointSize(16)
        self.txtQR.setFont(tempFont)

        self.txtQR.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

        self.btnBrowse.clicked.connect(self.browseForFile)

        self.btnBack.clicked.connect(self.backToEmail)
        self.btnNext.clicked.connect(self.goToPIN)

    def browseForFile(self):
        filter = "Images (*.png *.bmp *.jpg)"
        coverImageName = QFileDialog.getOpenFileNames(self, 'Get Cover Image', './', filter=filter)

        if len(coverImageName[0]) != 0:
            self.QRFilePath = coverImageName[0][0]
            self.txtQR.setPixmap(QPixmap(self.QRFilePath))
            self.txtQR.setScaledContents(True)
            print(decodeQR(self.QRFilePath))

    def verifyQR(self):
        print("Your QR Data:")

    def backToEmail(self):
        self.widgets.setCurrentIndex(1)

    def goToPIN(self):
        self.widgets.setCurrentIndex(3)
        self.allWidgets.widgetsObjects[3].tfPin1.setFocus()


class PINSignIn(QDialog):
    widgets: QStackedWidget

    def __init__(self, allWidgets):
        super(PINSignIn, self).__init__()
        loadUi('PIN Sign In.ui', self)
        self.widgets = allWidgets.widgets

        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

        self.btnBack.clicked.connect(self.backToQR)

        self.tfPin1.keyPressEvent = self.customKeyPressEvent1
        self.tfPin2.keyPressEvent = self.customKeyPressEvent2
        self.tfPin3.keyPressEvent = self.customKeyPressEvent3
        self.tfPin4.keyPressEvent = self.customKeyPressEvent4

    def customKeyPressEvent1(self, e):

        if -1<e.key()<256 and chr(e.key()).isnumeric():
            self.tfPin1.setText(chr(e.key()))
            self.tfPin2.setFocus()
        else:
            if e.key() == 16777219:  # backlash
                self.tfPin1.setText("")


    def customKeyPressEvent2(self, e):
        if -1<e.key()<256 and chr(e.key()).isnumeric():
            self.tfPin2.setText(chr(e.key()))
            self.tfPin3.setFocus()
        else:
            if e.key() == 16777219:#backlash
                self.tfPin2.setText("")
                self.tfPin1.setFocus()

    def customKeyPressEvent3(self, e):
        if -1<e.key()<256 and chr(e.key()).isnumeric():
            self.tfPin3.setText(chr(e.key()))
            self.tfPin4.setFocus()
        else:
            if e.key() == 16777219:#backlash
                self.tfPin3.setText("")
                self.tfPin2.setFocus()

    def customKeyPressEvent4(self, e):
        if -1<e.key()<256 and chr(e.key()).isnumeric():
            self.tfPin4.setText(chr(e.key()))
        else:
            if e.key() == 16777219:#backlash
                self.tfPin4.setText("")
                self.tfPin3.setFocus()
            else:
                if e.key() == 16777220:#enter
                  self.signIn()


    def signIn(self):
        print("TEST")
        self.widgets.setCurrentIndex(7)
        self.widgets.setFixedSize(QSize(1223, 685))

    def backToQR(self):
        self.widgets.setCurrentIndex(2)




class DraggableFilesQLabelQR(QLabel):

    def __init__(self, widget, QRScreen: QRSignIn):
        super(DraggableFilesQLabelQR, self).__init__(widget)

        self.QRScreen = QRScreen
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().text()
        file_path = re.sub('file:///', '', file_path)

        self.QRScreen.QRFilePath = file_path
        print(decodeQR(self.QRScreen.QRFilePath))

        self.setPixmap(QPixmap(self.QRFilePath))
        self.setScaledContents(True)
