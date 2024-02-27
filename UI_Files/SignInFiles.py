import re
import threading
from hashlib import sha256

import requests
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QStackedWidget, QLabel, QFileDialog, QLineEdit, QMessageBox
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
        if self.allWidgets.emailSignInValid:
            AuthenticateEmail.authenticated = True
            self.widgets.setCurrentIndex(2)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)

            msg.setText(
                "Invalid Email!\nBe sure to select an email with an account before continuing.")

            msg.setWindowTitle("Invalid Email!")

            msg.addButton(QMessageBox.Ok)

            retval = msg.exec_()

    def startTheThread(self):
        t = threading.Thread(daemon=True, name='AuthenticationFlow', target=openGmail, args=[self.updateUI])
        t.start()

    def updateUI(self):
        if AuthenticateEmail.currentEmail != "":
            URL = "https://localhost:44321/api/Users/CheckEmail"

            checkEmail = {"email": AuthenticateEmail.currentEmail}

            checkEmailRequest = requests.post(url=URL, json=checkEmail, verify=False)
            print(checkEmailRequest.text)
            if checkEmailRequest.status_code == 200:
                self.txtLoggedEmail.setText("Welcome\n" + AuthenticateEmail.currentEmail)
                self.allWidgets.emailSignIn = AuthenticateEmail.currentEmail
                self.allWidgets.emailSignInValid = True
            else:
                self.txtLoggedEmail.setText("Email not found!\nNo account has that email.")
                self.allWidgets.emailSignIn = ""
                self.allWidgets.emailSignInValid = False


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

    def cancelSignIn(self):
        AuthenticateEmail.authenticated = True
        self.allWidgets.abandonSignIn()

    def browseForFile(self):
        filter = "Images (*.png *.bmp *.jpg)"
        coverImageName = QFileDialog.getOpenFileNames(self, 'Get Cover Image', './', filter=filter)

        if len(coverImageName[0]) != 0:
            self.QRFilePath = coverImageName[0][0]
            self.allWidgets.QRSignInDirectory = self.QRFilePath
            self.txtQR.setPixmap(QPixmap(self.QRFilePath))
            self.txtQR.setScaledContents(True)
            print(decodeQR(self.QRFilePath))

    def verifyQR(self):
        QRData = decodeQR(self.allWidgets.QRSignInDirectory)
        QRdataSignature = sha256(QRData.encode("utf-8")).hexdigest()

        print(QRdataSignature)

        URL = "https://localhost:44321/api/Users/CheckQR"

        createUserBody = {"email": self.allWidgets.emailSignIn,
                          "qrSignature": QRdataSignature}

        checkQRRequest = requests.post(url=URL, json=createUserBody, verify=False)
        print(checkQRRequest.text)
        if checkQRRequest.status_code == 200:
            return True
        else:
            return False

    def backToEmail(self):

        self.widgets.setCurrentIndex(1)

    def goToPIN(self):
        if self.allWidgets.QRSignInDirectory == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)

            msg.setText(
                "You did not enter a QR!\nPlease select a QR.")

            msg.setWindowTitle("No QR!")

            msg.addButton(QMessageBox.Ok)

            retval = msg.exec_()
        else:
            if self.verifyQR():
                self.widgets.setCurrentIndex(3)
                self.allWidgets.widgetsObjects[3].tfPin1.setFocus()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)

                msg.setText(
                    "QR is not associated with this email!\nPlease enter the right QR code for this email.")

                msg.setWindowTitle("Incorrect QR!")

                msg.addButton(QMessageBox.Ok)

                retval = msg.exec_()


class PINSignIn(QDialog):
    widgets: QStackedWidget

    def __init__(self, allWidgets):
        super(PINSignIn, self).__init__()
        loadUi('PIN Sign In.ui', self)

        self.widgets = allWidgets.widgets
        self.allWidgets = allWidgets

        self.btnHome.clicked.connect(self.cancelSignIn)

        self.btnBack.clicked.connect(self.backToQR)

        self.btnSignIn.clicked.connect(self.signIn)

        self.tfPin1.keyPressEvent = self.customKeyPressEvent1
        self.tfPin2.keyPressEvent = self.customKeyPressEvent2
        self.tfPin3.keyPressEvent = self.customKeyPressEvent3
        self.tfPin4.keyPressEvent = self.customKeyPressEvent4

    def cancelSignIn(self):
        AuthenticateEmail.authenticated = True
        self.allWidgets.abandonSignIn()

    def customKeyPressEvent1(self, e):

        if -1 < e.key() < 256 and chr(e.key()).isnumeric():
            self.tfPin1.setText(chr(e.key()))
            self.tfPin2.setFocus()
        else:
            if e.key() == 16777219:  # backlash
                self.tfPin1.setText("")
            else:
                if (e.key() == 16777236):  # right arrow
                    self.tfPin2.setFocus()

    def customKeyPressEvent2(self, e):
        if -1 < e.key() < 256 and chr(e.key()).isnumeric():
            self.tfPin2.setText(chr(e.key()))
            self.tfPin3.setFocus()
        else:
            if e.key() == 16777219:  # backlash
                self.tfPin2.setText("")
                self.tfPin1.setFocus()
            else:
                if (e.key() == 16777236):  # right arrow
                    self.tfPin3.setFocus()
                else:
                    if (e.key() == 16777234):  # left arrow
                        self.tfPin1.setFocus()

    def customKeyPressEvent3(self, e):
        if -1 < e.key() < 256 and chr(e.key()).isnumeric():
            self.tfPin3.setText(chr(e.key()))
            self.tfPin4.setFocus()
        else:
            if e.key() == 16777219:  # backlash
                self.tfPin3.setText("")
                self.tfPin2.setFocus()
            else:
                if (e.key() == 16777236):  # right arrow
                    self.tfPin4.setFocus()
                else:
                    if (e.key() == 16777234):  # left arrow
                        self.tfPin2.setFocus()

    def customKeyPressEvent4(self, e):
        if -1 < e.key() < 256 and chr(e.key()).isnumeric():
            self.tfPin4.setText(chr(e.key()))
        else:
            if e.key() == 16777219:  # backlash
                self.tfPin4.setText("")
                self.tfPin3.setFocus()
            else:
                if e.key() == 16777220:  # enter
                    self.signIn()
                else:
                    if (e.key() == 16777234):  # left arrow
                        self.tfPin3.setFocus()

    def validatePIN(self):

        PINSignature = sha256(self.allWidgets.PINSignIN.encode("utf-8")).hexdigest()

        print(self.allWidgets.emailSignIn)
        print(PINSignature)

        URL = "https://localhost:44321/api/Users/CheckPIN"

        createUserBody = {"email": self.allWidgets.emailSignIn,
                          "pinSignature": PINSignature}

        checkPINRequest = requests.post(url=URL, json=createUserBody, verify=False)
        print(checkPINRequest.text)
        if checkPINRequest.status_code == 200:
            return True
        else:
            return False

    def signIn(self):
        self.allWidgets.PINSignIN = self.tfPin1.text() + self.tfPin2.text() + self.tfPin3.text() + self.tfPin4.text()
        if self.allWidgets.PINSignIN == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)

            msg.setText(
                "You did not choose a PIN!\nBe sure to create a PIN before signing up.")

            msg.setWindowTitle("No PIN!")

            msg.addButton(QMessageBox.Ok)

            retval = msg.exec_()

        else:
            if len(self.allWidgets.PINSignIN) < 4:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)

                msg.setText(
                    "Your Pin is not made up of 4 numbers!\nBe sure to add the rest of the PIN before continuing.")

                msg.setWindowTitle("Pin Incomplete!")

                msg.addButton(QMessageBox.Ok)

                retval = msg.exec_()

            else:
                if self.validatePIN():
                    self.widgets.setCurrentIndex(7)
                    self.widgets.setFixedSize(QSize(1223, 685))
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Critical)

                    msg.setText(
                        "PIN is not associated with this email!\nPlease enter the right PIN for this email.")

                    msg.setWindowTitle("Incorrect PIN!")

                    msg.addButton(QMessageBox.Ok)

                    retval = msg.exec_()

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
        self.QRScreen.allWidgets.QRSignInDirectory = file_path
        print(decodeQR(self.QRScreen.QRFilePath))

        self.setPixmap(QPixmap(self.QRScreen.QRFilePath))
        self.setScaledContents(True)
