from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QStackedWidget
from PyQt5.uic import loadUi


class EmailSignUp(QDialog):

    stackedWidget:QStackedWidget
    def __init__(self, stackedWidget):
        super(EmailSignUp, self).__init__()
        loadUi('Email Sign Up.ui', self)
        self.nextButton.clicked.connect(self.goToNumber)
        self.stackedWidget = stackedWidget

    def loginfunction(self):
        email = self.email.text()
        print("Successfully logged in with email:", email)
        verification = self.verification.text()
        print("Verification code sent as: " + verification)

    def verificationfunction(self):
        print("Verification code is: 42R6UM")

    def goToNumber(self):
        phone = PhoneSignUp()
        self.stackedWidget.addWidget(phone)
        self.stackedWidget.setCurrentIndex(6)




class PasswordSignUp(QDialog):
    def __init__(self, stacked_widget):
        super(PasswordSignUp, self).__init__()
        loadUi('Uis/passwdSignUp.ui', self)
        self.nextButton.clicked.connect(self.goToEmail)
        self.password.setEchoMode(QLineEdit.Password)
        self.repassword.setEchoMode(QLineEdit.Password)
        self.stacked_widget = stacked_widget

    def loginfunction(self):
        password = self.password.text()
        print("Successfully logged in with password:", password)

    def goToEmail(self):
        emailSignUp = EmailSignUp(self.stacked_widget)
        self.stacked_widget.addWidget(emailSignUp)
        self.stacked_widget.setCurrentIndex(5)

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class PhoneSignUp(QDialog):
    def __init__(self):
        super(PhoneSignUp, self).__init__()
        loadUi('Uis/phoneSignUp.ui', self)

    def loginfunction(self):
        phone = self.phone.text()
        print("Successfully logged in with phone:", phone)
        verification = self.verification.text()
        print("Verification code sent as: " + verification)

    def verificationfunction(self):
        print("Verification code is: 73R9TC")



