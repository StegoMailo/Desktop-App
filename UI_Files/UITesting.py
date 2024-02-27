import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt5.uic import loadUi

from Gmail import AuthenticateEmail

resources = exec(open("./Designer Resource Files/resources.py","r").read())

from UI_Files.ReceiveStegoMailFiles import Decryption, EmailStatus, ExtractStego
from UI_Files.SendStegoMailFiles import Encryption, AdvancedSettings, EmailInformation, SentEmailStatus
from UI_Files.SignInFiles import EmailSignIn, QRSignIn, PINSignIn
from UI_Files.SignUpFiles import EmailSignUp, QRSignUp, PINSignUp


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('Welcome Screen.ui', self)
        self.btnSignIn.clicked.connect(self.goToSignIn)
        self.btnSignUp.clicked.connect(self.goToSignUp)

    def goToSignIn(self):
        allWidgets.widgets.setCurrentIndex(1)

    def goToSignUp(self):
        allWidgets.widgets.setCurrentIndex(4)


class allWidgets():
    widgets: QStackedWidget
    widgetsObjects = []

    currentEmail:str

    emailSignUp = ""
    QRSignUpDirectory= ""
    PINSignUp= ""

    emailSignIn = ""
    QRSignInDirectory= ""
    PINSignIn= ""

    emailSignInValid = False
    QRSignInValid = False
    PINSignInValid = False

    emailSignUpValid = False


    encryptionKey:str
    seed:str
    isSoundUsed:bool
    saveStegoMedia:bool

    coverMediaPath:str
    secretFilePath:str

    stegoFile:str

    @staticmethod
    def abandonSignIn():
        allWidgets.emailSignIn = ""
        allWidgets.QRSignInDirectory = ""
        allWidgets.PINSignIn = ""

        allWidgets.emailSignInValid = False
        allWidgets.QRSignInValid = False
        allWidgets.PINSignInValid = False


        allWidgets.widgets.setCurrentIndex(0)

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[3])
        allWidgets.widgetsObjects[3].close()
        allWidgets.widgetsObjects[3] = PINSignIn(allWidgets)
        allWidgets.widgets.insertWidget(3, allWidgets.widgetsObjects[3])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[2])
        allWidgets.widgetsObjects[2].close()
        allWidgets.widgetsObjects[2] = QRSignIn(allWidgets)
        allWidgets.widgets.insertWidget(2, allWidgets.widgetsObjects[2])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[1])
        allWidgets.widgetsObjects[1].close()
        allWidgets.widgetsObjects[1] = EmailSignIn(allWidgets)
        allWidgets.widgets.insertWidget(1, allWidgets.widgetsObjects[1])

    @staticmethod
    def abandonSignUp():
        allWidgets.widgets.setCurrentIndex(0)

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[6])
        allWidgets.widgetsObjects[6].close()
        allWidgets.widgetsObjects[6] = PINSignUp(allWidgets)
        allWidgets.widgets.insertWidget(6, allWidgets.widgetsObjects[6])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[5])
        allWidgets.widgetsObjects[5].close()
        allWidgets.widgetsObjects[5] = QRSignUp(allWidgets)
        allWidgets.widgets.insertWidget(5, allWidgets.widgetsObjects[5])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[4])
        allWidgets.widgetsObjects[4].close()
        allWidgets.widgetsObjects[4] = EmailSignUp(allWidgets)
        allWidgets.widgets.insertWidget(4, allWidgets.widgetsObjects[4])

    #Go To encryption screens
    @staticmethod
    def goToEncryption():
        allWidgets.widgets.setCurrentIndex(7)
        allWidgets.widgets.setFixedSize(QSize(1223, 711))

    @staticmethod
    def goToStegoContent():
        allWidgets.widgets.setCurrentIndex(7)
        allWidgets.widgets.setFixedSize(QSize(1223, 711))
    @staticmethod
    def goToEmailInformation():
        allWidgets.widgets.setCurrentIndex(9)
        allWidgets.widgets.setFixedSize(QSize(1081, 711))

    #Go to decryption screens

    @staticmethod
    def goToDecryption():
        allWidgets.widgets.setCurrentIndex(11)
        allWidgets.widgets.setFixedSize(QSize(1223, 762))

    @staticmethod
    def goToEmailStatus():
        allWidgets.widgets.setCurrentIndex(12)#change to 12
        allWidgets.widgets.setFixedSize(QSize(1128, 762))

    @staticmethod
    def goToEmailStatusFromList(customItem):

        allWidgets.widgetsObjects[12].from_ = customItem.getSenderString()
        allWidgets.widgetsObjects[12].subject = customItem.getSubjectString()

        allWidgets.widgetsObjects[12].tfFrom .setText(allWidgets.widgetsObjects[12].from_)
        allWidgets.widgetsObjects[12].tfSubject.setText(allWidgets.widgetsObjects[12].subject)


        allWidgets.widgets.setCurrentIndex(12)  # change to 12
        allWidgets.widgets.setFixedSize(QSize(1128, 762))

    @staticmethod
    def goToEmailStatusFromUpload():
        allWidgets.widgets.setCurrentIndex(12)  # change to 12
        allWidgets.widgets.setFixedSize(QSize(1128, 762))


app = QApplication(sys.argv)

allWidgets.widgets = QtWidgets.QStackedWidget()
allWidgets.widgets.setWindowTitle("StegoMailo")
allWidgets.widgets.setWindowIcon(QtGui.QIcon('../favicon.png'))

welcomeScreen = WelcomeScreen()
allWidgets.widgetsObjects.append(welcomeScreen)
allWidgets.widgets.addWidget(welcomeScreen)  # index 0

emailSignIn = EmailSignIn(allWidgets)
allWidgets.widgetsObjects.append(emailSignIn)
allWidgets.widgets.addWidget(emailSignIn)  # index 1

QrSignIn = QRSignIn(allWidgets)
allWidgets.widgetsObjects.append(QrSignIn)
allWidgets.widgets.addWidget(QrSignIn)  # index 2

PinSignIn = PINSignIn(allWidgets)
allWidgets.widgetsObjects.append(PinSignIn)
allWidgets.widgets.addWidget(PinSignIn)  # index 3

emailSignUp = EmailSignUp(allWidgets)
allWidgets.widgetsObjects.append(emailSignUp)
allWidgets.widgets.addWidget(emailSignUp)  # index 4

QrSignUp = QRSignUp(allWidgets)
allWidgets.widgetsObjects.append(QrSignUp)
allWidgets.widgets.addWidget(QrSignUp)  # index 5

PinSignUp = PINSignUp(allWidgets)
allWidgets.widgetsObjects.append(PinSignUp)
allWidgets.widgets.addWidget(PinSignUp)  # index 6

encryption = Encryption(allWidgets)
allWidgets.widgetsObjects.append(encryption)
allWidgets.widgets.addWidget(encryption)  # index 7

advancedSettings = AdvancedSettings(allWidgets)
allWidgets.widgetsObjects.append(advancedSettings)
allWidgets.widgets.addWidget(advancedSettings)  # index 8

emailInformation = EmailInformation(allWidgets)
allWidgets.widgetsObjects.append(emailInformation)
allWidgets.widgets.addWidget(emailInformation)  # index 9

sendStegoMail = SentEmailStatus(allWidgets)
allWidgets.widgetsObjects.append(sendStegoMail)
allWidgets.widgets.addWidget(sendStegoMail)  # index 10

decryption = Decryption(allWidgets)
allWidgets.widgetsObjects.append(decryption)
allWidgets.widgets.addWidget(decryption)  # index 11

emailStatus = EmailStatus(allWidgets)
allWidgets.widgetsObjects.append(emailStatus)
allWidgets.widgets.addWidget(emailStatus)#index 12

extractStego = ExtractStego(allWidgets)
allWidgets.widgetsObjects.append(extractStego)
allWidgets.widgets.addWidget(extractStego)#index 13

allWidgets.widgets.setFixedWidth(520)
allWidgets.widgets.setFixedHeight(630)

allWidgets.widgets.setCurrentIndex((0))

allWidgets.widgets.show()

app.exec_()
