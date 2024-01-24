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
        reenteredPassword = self.tfReenterPassword.text()
        print("Your Password Is:" + password)
        print("Your second Password Is:" + reenteredPassword)
        self.btnNext.setHidden(False)

    def backToEmail(self):
        self.widgets.setCurrentIndex(4)

    def goToPhoneNumber(self):
        self.widgets.setCurrentIndex(6)


class PhoneSignUp(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(PhoneSignUp, self).__init__()
        loadUi('Phone Sign Up.ui', self)
        self.stackedWidget = allWidgets.widgets
        self.widgets = allWidgets.widgets

        self.btnAbandon.clicked.connect(allWidgets.abandonSignIn)

        self.btnSignIn.clicked.connect(self.signIn)

        self.btnSendCode.clicked.connect(self.sendVerifcationCode)

        self.btnVerifyCode.clicked.connect(self.verifyCode)

        self.btnSignIn.setHidden(True)

        self.btnBack.clicked.connect(self.backToPassword)

    def sendVerifcationCode(self):
        phoneNumber = self.tfPhoneNumber.text()
        print("Phone Code sent was 123124124312 to:" + phoneNumber)
        self.btnSendCode.setHidden(True)

    def verifyCode(self):
        print("Code is Valid")
        self.btnSendCode.setHidden(False)
        self.btnSignIn.setHidden(False)

    def signIn(self):
        phoneNumber = self.tfPhoneNumber.text()
        print("Successfully logged in with phone:", phoneNumber)

    def backToPassword(self):
        self.widgets.setCurrentIndex(5)

