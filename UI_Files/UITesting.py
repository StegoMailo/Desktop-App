import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt5.uic import loadUi

from UI_Files.SignInFiles import EmailSignIn, PasswordSignIn


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('Welcome Screen.ui', self)
        self.btnSignIn.clicked.connect(self.goToSignIn)
        self.btnSignIn.clicked.connect(self.goToSignUp)

    def goToSignIn(self):
        widgets.setCurrentIndex(1)

    def goToSignUp(self):
        widgets.setCurrentIndex(4)


app = QApplication(sys.argv)
widgets = QtWidgets.QStackedWidget()

welcomeScreen = WelcomeScreen()
widgets.addWidget(welcomeScreen)  # index 0

emailSignIn = EmailSignIn(widgets)
widgets.addWidget(emailSignIn)# index 1

passwordSignIn = PasswordSignIn(widgets)
widgets.addWidget(passwordSignIn)# index 2

widgets.setFixedWidth(494)
widgets.setFixedHeight(629)
widgets.show()
app.exec_()
