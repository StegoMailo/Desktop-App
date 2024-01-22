from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class EmailSignIn(QDialog):
    def __init__(self, stacked_widget):
        super(EmailSignIn, self).__init__()
        loadUi('Email Sign In.ui', self)

        stacked_widget.setFixedWidth(520)
        stacked_widget.setFixedHeight(620)
        self.stacked_widget = stacked_widget

        self.btnNext.clicked.connect(self.goToPhoneNumber)

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
        self.stacked_widget.setCurrentIndex(2)


class PasswordSignIn(QDialog):
    def __init__(self, stacked_widget):
        super(PasswordSignIn, self).__init__()
        loadUi('Password Sign In.ui', self)

        stacked_widget.setFixedWidth(520)
        stacked_widget.setFixedHeight(620)
        self.stacked_widget = stacked_widget


        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.btnNext.clicked.connect(self.goToPhoneNumber)
        self.btnVerifyPassword.clicked.connect(self.goToPhoneNumber)
        self.btnBack.clicked.connect(self.goToPhoneNumber)


    def verifyPassword(self):
        password = self.tfPassword.text()
        print("Your Password Is:" + password)

    def backToEmail(self):
        self.stacked_widget.setCurrentIndex(1)


    def goToPhoneNumber(self):
        self.stacked_widget.setCurrentIndex(2)


class PhoneSignIn(QDialog):
    def __init__(self):
        super(PhoneSignIn, self).__init__()
        loadUi('phoneSignIn.ui', self)

    def loginfunction(self):
        phone = self.phone.text()
        print("Successfully logged in with phone:", phone)
        verification = self.verification.text()
        print("Verification code sent as: " + verification)

    def verificationfunction(self):
        print("Verification code is: 73R9TC")
