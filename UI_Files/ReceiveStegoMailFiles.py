##########################################################################################################
import sys
import threading
import time

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QStackedWidget, QFileDialog, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QFrame, QMessageBox
from PyQt5.uic import loadUi


# Decryption Ui : it has three interfaces (Main Decryption , EmailStatus_Decryption ,ExtractEmailContent_Decryption)

class QCustomQWidget(QWidget):
    subject: str
    sender: str

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)

        self.textQHBoxLayout = QHBoxLayout()

        self.txtSubject = QLabel()
        self.txtSender = QLabel()
        self.textQHBoxLayout.addWidget(self.txtSubject)
        self.textQHBoxLayout.addWidget(self.txtSender)
        self.allQVBoxLayout = QVBoxLayout()
        self.allQVBoxLayout.addLayout(self.textQHBoxLayout, 1)
        self.setLayout(self.allQVBoxLayout)

        font = self.txtSubject.font()

        font.setPointSize(16)

        self.txtSubject.setFont(font)
        self.txtSender.setFont(font)

        self.txtSubject.setStyleSheet('''
            color: rgb(0, 0, 255);
            background-color: rgba(0,0,0,0);
        ''')
        self.txtSender.setStyleSheet('''
            color: rgb(255, 0, 0);
            background-color: rgba(0,0,0,0);
        ''')

    def setSubject(self, text):
        self.txtSubject.setText(text)
        self.subject = text

    def setSender(self, text):
        self.txtSender.setText(text)
        self.sender = text

    def getSubjectString(self):
        return self.subject

    def getSenderString(self):
        return self.sender


class Decryption(QDialog):
    stegoFile: str
    stackedWidget: QStackedWidget
    testList = [("hi", "Taha"), ("Iloveshwarma", "Izzat"), ("what's up bro", "Fathi")]

    def __init__(self, allWidgets):
        super(Decryption, self).__init__()
        loadUi("Decryption.ui", self)

        self.allWidgets = allWidgets
        self.stackedWidget = allWidgets.widgets

        self.btnUploadStego.clicked.connect(self.uploadFile)

        self.btnEmailStatus.clicked.connect(self.goToEmailStatus)

        self.btnEmailContent.clicked.connect(self.goToEmailContent)
        self.btnEncryption.clicked.connect(self.goToEncryption)
        self.btnStegoContent.clicked.connect(self.goToStegoContent)

        # self.lwEmails.itemClicked.connect(self.goToEmailStatusFromList)

        self.fillList()
        self.lwEmails.itemClicked.connect(self.goToEmailStatusFromList)
        # QListWidget.

    def fillList(self):
        for subject, sender in self.testList:
            customListItem = QCustomQWidget()
            customListItem.setSubject(subject)
            customListItem.setSender(sender)

            myQListWidgetItem = QListWidgetItem(self.lwEmails)
            myQListWidgetItem.setSizeHint(customListItem.sizeHint())

            self.lwEmails.addItem(myQListWidgetItem)
            self.lwEmails.setItemWidget(myQListWidgetItem, customListItem)

    def goToEmailStatus(self):
        self.allWidgets.goToEmailStatus()

    def goToEmailStatusFromList(self, item: QListWidgetItem):

        customItem = self.lwEmails.itemWidget(item)

        print(customItem.getSubjectString() + "  " + customItem.getSenderString())

        self.allWidgets.goToEmailStatusFromList(customItem)

    def goToStegoContent(self):  # go to  stego content UI
        self.allWidgets.goToStegoContent()

    def goToEncryption(self):
        self.allWidgets.goToEncryption()

    def goToEmailContent(self):
        self.allWidgets.goToEmailInformation()

    def uploadFile(self):
        # Open a file dialog to choose a file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)  # Allow selecting an existing file
        file_path, _ = file_dialog.getOpenFileName(self, 'Choose a file', '', 'All Files (*);;Text Files (*.txt)')

        if file_path:
            self.allWidgets.secretFilePath = file_path
            self.allWidgets.goToEmailStatusFromUpload()
            print(f'Selected File: {file_path}')


class EmailStatus(QDialog):
    stackedWidget: QStackedWidget

    from_ = "From: "
    fileName = "File Name:"
    subject = "Subject:"


    def __init__(self, allWidgets):
        super(EmailStatus, self).__init__()
        loadUi("Stego File Information.ui", self)

        self.allWidgets = allWidgets
        self.stackedWidget = allWidgets.widgets

        self.btnEncryption.clicked.connect(self.goToEncryption)
        self.btnStegoContent.clicked.connect(self.goToStegoContent)
        self.btnEmailContent.clicked.connect(self.goToEmailInformation)

        self.btnDecryption.clicked.connect(self.goToDecryption)
        self.btnExtract.clicked.connect(self.extractStegoFile)


    def goToStegoContent(self):  # go to  Stego content UI
        self.allWidgets.goToStegoContent()

    def goToEncryption(self):  # go to  Gmail content UI
        self.allWidgets.goToEncryption()

    def goToDecryption(self):
        self.allWidgets.goToDecryption()

    def goToEmailInformation(self):
        self.allWidgets.goToEmailInformation()

    def extractStegoFile(self):
        self.stackedWidget.setCurrentIndex(13)
        self.allWidgets.widgetsObjects[13].encodeStegoFile()
        self.stackedWidget.setFixedSize(QSize(752, 319))


class ExtractStego(QDialog):
    stackedWidget: QStackedWidget

    cancelled = False
    paused = False

    def __init__(self, allWidgets):
        super(ExtractStego, self).__init__()
        loadUi("Extracting Stego.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.allWidgets = allWidgets

        self.btnCancel.clicked.connect(self.cancelStegoMail)

    def cancelStegoMail(self):

        self.paused = True

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("Are you sure you want to cancel sending your Stego Mail?\n")

        msg.setWindowTitle("Are you sure you want to cancel?")

        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)

        retval = msg.exec_()

        if retval == QMessageBox.Yes:
            self.cancelled = True
            self.paused = False

            self.allWidgets.goToStegoContent()


        else:
            self.paused = False

        print(QMessageBox.Yes)

    def encodeStegoFile(self):
        progress = 0
        t1 = threading.Thread(target=self.count, daemon=True, kwargs={'progress': progress})
        t1.start()

        self.startTheThread()

    def startTheThread(self):
        self.cancelled = False
        self.paused = False

        t = threading.Thread(daemon=True, name='StatusThread', target=testingTreads,
                             args=[self.updateUI, self])
        t.start()

    def updateUI(self, progress):
        print(progress)
        self.progressBar.setValue(progress)

    def count(self, progress):
        while not self.cancelled:
            while self.paused:
                continue
            time.sleep(1)
            progress += 1
            print("Hi")
        sys.exit()


class Communicate(QObject):
    myGUI_signal = pyqtSignal(int)


def testingTreads(callbackFunc, sentEmail):
    mySrc = Communicate()
    mySrc.myGUI_signal.connect(callbackFunc)

    progress = 0
    while not sentEmail.cancelled:
        while sentEmail.paused:
            continue
        time.sleep(1)
        progress += 1
        mySrc.myGUI_signal.emit(progress)
    mySrc.myGUI_signal.emit(0)

