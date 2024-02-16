from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QStackedWidget, QMessageBox
from PyQt5.uic import loadUi



class EmailSignIn(QDialog):
    widgets:QStackedWidget
    def __init__(self,allWidgets):
        super(EmailSignIn, self).__init__()
        loadUi('Email Sign In.ui', self)

        self.widgets = allWidgets.widgets

        self.btnNext.clicked.connect(self.goToPhoneNumber)

        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

        self.btnSendCode.clicked.connect(self.SendVerificationCode)

        self.btnVerify.clicked.connect(self.VerifyCode)

        self.txtSignInEmailVerification.setHidden(True)
        self.tfVerificationCode.setHidden(True)

        self.btnVerify.setHidden(True)

        self.btnNext.setHidden(True)

    def SendVerificationCode(self):

        codeToSend = "1232131" #generate Code
        print("Code Sent Is: "+codeToSend)

        self.btnSendCode.setHidden(True)
        self.txtSignInEmailVerification.setHidden(False)
        self.tfVerificationCode.setHidden(False)
        self.btnVerify.setHidden(False)

    def VerifyCode(self):
        verification = self.tfVerificationCode.text()
        codeToSend=""
        if verification == codeToSend:
            print("Verified")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText("Shawarma!")

            msg.setWindowTitle("Invalid Key")

            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()



        print("Verification code sent as: " + verification)

        self.btnSendCode.setHidden(False)
        self.btnNext.setHidden(False)

    def goToPhoneNumber(self):
        self.widgets.setCurrentIndex(2)





class PasswordSignIn(QDialog):
    widgets:QStackedWidget
    def __init__(self,allWidgets):
        super(PasswordSignIn, self).__init__()
        loadUi('Password Sign In.ui', self)
        self.widgets = allWidgets.widgets

        self.tfPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

        self.btnVerifyPassword.clicked.connect(self.verifyPassword)

        self.btnBack.clicked.connect(self.backToEmail)
        self.btnNext.clicked.connect(self.goToPhoneNumber)

        self.btnNext.setHidden(True)

    def verifyPassword(self):
        password = self.tfPassword.text()
        print("Your Password Is:" + password)
        self.btnNext.setHidden(False)

    def backToEmail(self):
        self.widgets.setCurrentIndex(1)

    def goToPhoneNumber(self):
        self.widgets.setCurrentIndex(3)





class PhoneSignIn(QDialog):
    widgets: QStackedWidget

    def __init__(self,allWidgets):
        super(PhoneSignIn, self).__init__()
        loadUi('Phone Sign In.ui', self)
        self.widgets = allWidgets.widgets

        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

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
        self.widgets.setCurrentIndex(7)
        self.widgets.setFixedSize(QSize(1223,685))

    def backToPassword(self):
        self.widgets.setCurrentIndex(2)






