import re
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QStackedWidget, QMessageBox, QLabel
from PyQt5.uic import loadUi

from Gmail import AuthenticateEmail
from Gmail.AuthenticateEmail import authenticateUser


class DraggableFilesQLabelQR(QLabel):
    QRFilePath = ""
    def __init__(self, widget):
        super(DraggableFilesQLabelQR, self).__init__(widget)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().text()
        file_path = re.sub('file:///', '', file_path)
        self.QRFilePath = file_path

        self.setPixmap(QPixmap(self.QRFilePath))
        self.setScaledContents(True)




class EmailSignIn(QDialog):
    widgets:QStackedWidget
    def __init__(self,allWidgets):
        super(EmailSignIn, self).__init__()
        loadUi('Email Sign In.ui', self)

        self.widgets = allWidgets.widgets

        self.btnGmail.clicked.connect(self.LogInToGmail)
        self.btnNext.clicked.connect(self.goToQR)

        self.btnHome.clicked.connect(allWidgets.abandonSignIn)



    def LogInToGmail(self):

        authenticateUser()

        if AuthenticateEmail.currentEmail != "":
            self.txtLoggedEmail.setText("Welcome\n" + AuthenticateEmail.currentEmail)

    def encodeStegoFile(self):
        progress = 0
        t1 = threading.Thread(target=self.count, daemon=True, kwargs={'progress': progress})
        t1.start()

        self.startTheThread(self)
    def goToQR(self):
        self.widgets.setCurrentIndex(2)

    def startTheThread(self, progress):
        self.cancelled = False
        self.paused = False

        t = threading.Thread(daemon=True, name='StatusThread', target=testingTreads,
                             args=[self.updateUI, progress])
        t.start()

    def updateUI(self, progress):
        self.progressBar.setValue(progress)

    def count(self, progress):
        progress += 1



class Communicate(QObject):
    myGUI_signal = pyqtSignal(int)


def testingTreads(callbackFunc, sentEmail):
    mySrc = Communicate()
    mySrc.myGUI_signal.connect(callbackFunc)

    progress = 0
    while not sentEmail.cancelled:
        while sentEmail.paused:
            continue

        progress += 1
        mySrc.myGUI_signal.emit(progress)
        
    mySrc.myGUI_signal.emit(0)

class QRSignIn(QDialog):
    widgets:QStackedWidget
    def __init__(self,allWidgets):
        super(QRSignIn, self).__init__()
        loadUi('QR Sign In.ui', self)
        self.widgets = allWidgets.widgets

        self.txtQR = DraggableFilesQLabelQR(self)

        self.txtQR.setStyleSheet(
            "background-color: rgba(138, 198, 253,0.5);   border-radius:10px; border: 0.5px solid #000000;"
            " color: rgb(0,0,0);")


        self.txtQR.setGeometry(140, 280, 251, 221)
        self.txtQR.setText("Drop Your\nQR Code Here")

        tempFont = self.txtQR.font()
        tempFont.setBold(False)
        tempFont.setPointSize(16)
        self.txtQR.setFont(tempFont)

        self.txtQR.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)


        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

        self.btnBack.clicked.connect(self.backToEmail)
        self.btnNext.clicked.connect(self.goToPhoneNumber)

        self.btnNext.setHidden(True)

    def verifyQR(self):
        print("Your QR Data:")

    def backToEmail(self):
        self.widgets.setCurrentIndex(1)

    def goToPhoneNumber(self):
        self.widgets.setCurrentIndex(3)





class PINSignIn(QDialog):
    widgets: QStackedWidget

    def __init__(self,allWidgets):
        super(PINSignIn, self).__init__()
        loadUi('PIN Sign In.ui', self)
        self.widgets = allWidgets.widgets



        self.btnHome.clicked.connect(allWidgets.abandonSignIn)

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






