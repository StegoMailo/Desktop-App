import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt5.uic import loadUi

from UI_Files.SignInFiles import PasswordSignIn, PhoneSignIn,EmailSignIn
from UI_Files.SignUpFiles import EmailSignUp, PasswordSignUp, PhoneSignUp


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
    widgets:QStackedWidget
    widgetsObjects = []

    @staticmethod
    def abandonSignIn():
        allWidgets.widgets.setCurrentIndex(0)



        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[3])
        allWidgets.widgetsObjects[3].close()
        allWidgets.widgetsObjects[3] = PhoneSignIn(allWidgets)
        allWidgets.widgets.insertWidget(3, allWidgets.widgetsObjects[3])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[2])
        allWidgets.widgetsObjects[2].close()
        allWidgets.widgetsObjects[2] = PasswordSignIn(allWidgets)
        allWidgets.widgets.insertWidget(2, allWidgets.widgetsObjects[2])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[1])
        allWidgets.widgetsObjects[1].close()
        allWidgets.widgetsObjects[1] = EmailSignIn(allWidgets)
        allWidgets.widgets.insertWidget(1, allWidgets.widgetsObjects[1])\

    @staticmethod
    def abandonSignUp():
        allWidgets.widgets.setCurrentIndex(0)

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[6])
        allWidgets.widgetsObjects[6].close()
        allWidgets.widgetsObjects[6] = PhoneSignUp(allWidgets)
        allWidgets.widgets.insertWidget(6, allWidgets.widgetsObjects[6])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[5])
        allWidgets.widgetsObjects[5].close()
        allWidgets.widgetsObjects[5] = PasswordSignUp(allWidgets)
        allWidgets.widgets.insertWidget(5, allWidgets.widgetsObjects[5])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[4])
        allWidgets.widgetsObjects[4].close()
        allWidgets.widgetsObjects[4] = EmailSignUp(allWidgets)
        allWidgets.widgets.insertWidget(4, allWidgets.widgetsObjects[4])


app = QApplication(sys.argv)

allWidgets.widgets = QtWidgets.QStackedWidget()

welcomeScreen = WelcomeScreen()
allWidgets.widgetsObjects.append(welcomeScreen)
allWidgets.widgets.addWidget(welcomeScreen)  # index 0

emailSignIn = EmailSignIn(allWidgets)
allWidgets.widgetsObjects.append(emailSignIn)
allWidgets.widgets.addWidget(emailSignIn)# index 1

passwordSignIn = PasswordSignIn(allWidgets)
allWidgets.widgetsObjects.append(passwordSignIn)
allWidgets.widgets.addWidget(passwordSignIn)# index 2

phoneNumberSignIn = PhoneSignIn(allWidgets)
allWidgets.widgetsObjects.append(phoneNumberSignIn)
allWidgets.widgets.addWidget(phoneNumberSignIn)# index 3

emailSignUp = EmailSignUp(allWidgets)
allWidgets.widgetsObjects.append(emailSignUp)
allWidgets.widgets.addWidget(emailSignUp)# index 4

passwordSignUp = PasswordSignUp(allWidgets)
allWidgets.widgetsObjects.append(passwordSignUp)
allWidgets.widgets.addWidget(passwordSignUp)# index 5

phoneNumberSignUp = PhoneSignUp(allWidgets)
allWidgets.widgetsObjects.append(phoneNumberSignUp)
allWidgets.widgets.addWidget(phoneNumberSignUp)# index 6

allWidgets.widgets.setFixedWidth(520)
allWidgets.widgets.setFixedHeight(630)

allWidgets.widgets.show()
app.exec_()
