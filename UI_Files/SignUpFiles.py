from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QStackedWidget
from PyQt5.uic import loadUi


class EmailSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(EmailSignUp, self).__init__()
        loadUi('Email Sign Up.ui', self)

        self.widgets = allWidgets.widgets

        self.btnNext.clicked.connect(self.goToPhoneNumber)

        self.btnAbandon.clicked.connect(allWidgets.abandonSignUp)

        self.btnSendCode.clicked.connect(self.SendVerificationCode)

        self.btnVerify.clicked.connect(self.VerifyCode)

        self.txtSignInEmailVerification.setHidden(True)
        self.tfVerificationCode.setHidden(True)

        self.btnVerify.setHidden(True)

        self.btnNext.setHidden(True)

    def SendVerificationCode(self):
        self.btnSendCode.setHidden(True)
        print("Code Sent Is: 42R6UM")

        self.txtSignInEmailVerification.setHidden(False)
        self.tfVerificationCode.setHidden(False)
        self.btnVerify.setHidden(False)

    def VerifyCode(self):
        verification = self.tfVerificationCode.text()
        print("Verification code sent as: " + verification)

        self.btnSendCode.setHidden(False)
        self.btnNext.setHidden(False)

    def goToPhoneNumber(self):
        self.widgets.setCurrentIndex(5)


class PasswordSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(PasswordSignUp, self).__init__()
        loadUi('Password Sign Up.ui', self)
        self.widgets = allWidgets.widgets

        self.tfPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        self.btnAbandon.clicked.connect(allWidgets.abandonSignUp)

        self.btnConfirm.clicked.connect(self.confirmPassword)

        self.btnBack.clicked.connect(self.backToEmail)
        self.btnNext.clicked.connect(self.goToPhoneNumber)

        self.btnNext.setHidden(True)

    def confirmPassword(self):
        password = self.tfPassword.text()
        reenteredPassword = self.tfReenteredPasssword.text()
        print("Your Password Is:" + password)
        print("Your second Password Is:" + reenteredPassword)
        self.btnNext.setHidden(False)

    def backToEmail(self):
        self.widgets.setCurrentIndex(4)

    def goToPhoneNumber(self):
        self.widgets.setCurrentIndex(5)


class PhoneSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(PhoneSignUp, self).__init__()
        loadUi('phoneSignUp.ui', self)
        self.stackedWidget = allWidgets.widgets

    def loginfunction(self):
        phone = self.phone.text()
        print("Successfully logged in with phone:", phone)
        verification = self.verification.text()
        print("Verification code sent as: " + verification)

    def verificationfunction(self):
        print("Verification code is: 73R9TC")
