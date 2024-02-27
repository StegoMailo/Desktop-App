import threading
from hashlib import sha256
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QStackedWidget, QMessageBox
from PyQt5.uic import loadUi

from Authentication.GenerateQR import generateQR
from Authentication.ReadQR import decodeQR
from Gmail import AuthenticateEmail
from Gmail.AuthenticateEmail import authenticateUser


class EmailSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(EmailSignUp, self).__init__()
        loadUi('Email Sign Up.ui', self)

        self.widgets = allWidgets.widgets
        self.allWidgets = allWidgets

        self.btnNext.clicked.connect(self.goToQR)

        self.btnHome.clicked.connect(self.cancelSignUp)

        self.btnGmail.clicked.connect(self.SignUpToGmail)

    def cancelSignUp(self):
        AuthenticateEmail.authenticated = True
        self.allWidgets.abandonSignUp()

    def SignUpToGmail(self):
        self.startTheThread()

    def startTheThread(self):
        t = threading.Thread(daemon=True, name='AuthenticationFlow', target=openGmail, args=[self.updateUI])
        t.start()

    def updateUI(self):
        if AuthenticateEmail.currentEmail != "":
            URL = "https://localhost:44321/api/Users/GetByEmail/"
            request = requests.get(url=URL+ AuthenticateEmail.currentEmail, verify=False)

            if request.status_code == 404:
                self.txtLoggedEmail.setText("You Chose:\n" + AuthenticateEmail.currentEmail)
                self.allWidgets.emailSignUp = AuthenticateEmail.currentEmail
                self.allWidgets.emailSignUpValid = True
            else:
                self.txtLoggedEmail.setText("Email in use!\nChoose a different email.")
                self.allWidgets.emailSignUp = ""
                self.allWidgets.emailSignUpValid = False



    def goToQR(self):
        if self.allWidgets.emailSignUpValid:
            AuthenticateEmail.authenticated = True
            self.widgets.setCurrentIndex(5)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)

            msg.setText(
                "You did not chose a valid email!\nBe sure to select an email for your account before continuing.")

            msg.setWindowTitle("No Valid Email!")

            msg.addButton(QMessageBox.Ok)

            retval = msg.exec_()


class Communicate(QObject):
    myGUI_signal = pyqtSignal()


def openGmail(callbackFunc):
    mySrc = Communicate()
    mySrc.myGUI_signal.connect(callbackFunc)
    authenticateUser()

    while not AuthenticateEmail.authenticated:
        continue
    mySrc.myGUI_signal.emit()


class QRSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(QRSignUp, self).__init__()
        loadUi('QR Sign Up.ui', self)
        self.widgets = allWidgets.widgets
        self.allWidgets = allWidgets

        self.btnBrowse.clicked.connect(self.loadQRDir)

        self.btnHome.clicked.connect(self.cancelSignUp)

        self.btnBack.clicked.connect(self.backToEmail)
        self.btnNext.clicked.connect(self.goToPin)

    def cancelSignUp(self):
        AuthenticateEmail.authenticated = True
        self.allWidgets.abandonSignUp()

    def loadQRDir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Set Output Destination", './')

        if len(directory) != 0:
            self.allWidgets.QRSignUpDirectory = directory
            self.txtQRLocation.setText("Location: " + directory)

    def backToEmail(self):
        self.widgets.setCurrentIndex(4)

    def goToPin(self):
        if self.allWidgets.QRSignUpDirectory == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)

            msg.setText(
                "You did not select a QR directory!\nBe sure to select a directory for the QR before continuing.")

            msg.setWindowTitle("No QR Directory!")

            msg.addButton(QMessageBox.Ok)

            retval = msg.exec_()

        else:
            self.widgets.setCurrentIndex(6)


class PINSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(PINSignUp, self).__init__()
        loadUi('PIN Sign Up.ui', self)

        self.widgets = allWidgets.widgets
        self.allWidgets = allWidgets

        self.tfPin1.keyPressEvent = self.customKeyPressEvent1
        self.tfPin2.keyPressEvent = self.customKeyPressEvent2
        self.tfPin3.keyPressEvent = self.customKeyPressEvent3
        self.tfPin4.keyPressEvent = self.customKeyPressEvent4

        self.btnHome.clicked.connect(self.cancelSignUp)

        self.btnSignUp.clicked.connect(self.signUp)

        self.btnBack.clicked.connect(self.backToQR)

    def cancelSignUp(self):
        AuthenticateEmail.authenticated = True
        self.allWidgets.abandonSignUp()

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
                    self.signUp()
                else:
                    if (e.key() == 16777234):  # left arrow
                        self.tfPin3.setFocus()

    def signUp(self):
        if self.allWidgets.emailSignUp == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)

            msg.setText("You did not select an email!\nBe sure to select an email before signing up.")

            msg.setWindowTitle("No Email!")

            msg.addButton(QMessageBox.Ok)

            retval = msg.exec_()



        else:
            if self.allWidgets.QRSignUpDirectory == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)

                msg.setText(
                    "You did not select a QR directory!\nBe sure to select a directory for the QR before signing up.")

                msg.setWindowTitle("No QR!")

                msg.addButton(QMessageBox.Ok)

                retval = msg.exec_()

            else:
                self.allWidgets.PINSignUp = self.tfPin1.text() + self.tfPin2.text() + self.tfPin3.text() + self.tfPin4.text()
                if self.allWidgets.PINSignUp == "":
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Critical)

                    msg.setText(
                        "You did not choose a PIN!\nBe sure to create a PIN before signing up.")

                    msg.setWindowTitle("No PIN!")

                    msg.addButton(QMessageBox.Ok)

                    retval = msg.exec_()

                else:
                    if len(self.allWidgets.PINSignUp) < 4:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Icon.Critical)

                        msg.setText(
                            "Your Pin is not made up of 4 numbers!\nBe sure to add the rest of the PIN before continuing.")

                        msg.setWindowTitle("Pin Incomplete!")

                        msg.addButton(QMessageBox.Ok)

                        retval = msg.exec_()

                    else:

                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Icon.Information)

                        msg.setText(
                            "Are you sure of the information you inputted?\nYour Email: " + self.allWidgets.emailSignUp +
                            "\nYour QR Directory: " + self.allWidgets.QRSignUpDirectory + "\n Your PIN: " + self.allWidgets.PINSignUp)

                        msg.setWindowTitle("Are you sure?")

                        msg.addButton(QMessageBox.Yes)
                        msg.addButton(QMessageBox.No)

                        retval = msg.exec_()

                        if retval == QMessageBox.Yes:
                            generateQR(self.allWidgets.QRSignUpDirectory + "/")
                            QRdata = decodeQR(self.allWidgets.QRSignUpDirectory + "/userQR.png")

                            QRdataSignature = sha256(QRdata.encode("utf-8")).hexdigest()

                            PINSignature = sha256(self.allWidgets.PINSignUp.encode("utf-8")).hexdigest()

                            URL = "https://localhost:44321/api/Users/AddUser"

                            createUserBody = {"email": self.allWidgets.emailSignUp,
                                              "qrSignature": QRdataSignature,
                                              "pinSignature": PINSignature}

                            createUserRequest = requests.post(url=URL, json=createUserBody, verify=False)
                            userPrivateKey = createUserRequest.text

                            with open("../TestFiles/"+self.allWidgets.emailSignUp + "_PrivateKey.txt", "w") as f:
                                f.write(userPrivateKey)

                            self.allWidgets.PINSignUp =""
                            self.allWidgets.QRSignUpDirectory = ""
                            self.allWidgets.emailSignUp = ""

                            self.allWidgets.emailSignUpValid = False


                            self.widgets.setCurrentIndex(7)
                            self.widgets.setFixedSize(QSize(1223, 685))

    def backToQR(self):
        self.widgets.setCurrentIndex(5)
