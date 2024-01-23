import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt5.uic import loadUi

from UI_Files.SignInFiles import PasswordSignIn, PhoneSignIn,EmailSignIn


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('Welcome Screen.ui', self)
        self.btnSignIn.clicked.connect(self.goToSignIn)
        self.btnSignIn.clicked.connect(self.goToSignUp)

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
        print("TEST")

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[2])
        allWidgets.widgetsObjects[2].close()
        allWidgets.widgetsObjects[2] = PasswordSignIn(allWidgets)
        allWidgets.widgets.insertWidget(2, allWidgets.widgetsObjects[2])

        allWidgets.widgets.removeWidget(allWidgets.widgetsObjects[1])
        allWidgets.widgetsObjects[1].close()
        allWidgets.widgetsObjects[1] = EmailSignIn(allWidgets)
        allWidgets.widgets.insertWidget(1, allWidgets.widgetsObjects[1])


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

phoneNumber = PhoneSignIn(allWidgets)
allWidgets.widgetsObjects.append(phoneNumber)
allWidgets.widgets.addWidget(phoneNumber)# index 3

allWidgets.widgets.setFixedWidth(520)
allWidgets.widgets.setFixedHeight(630)

allWidgets.widgets.show()
app.exec_()
