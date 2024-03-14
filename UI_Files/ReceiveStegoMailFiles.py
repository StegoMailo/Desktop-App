import sys
import threading
import time

from PyQt5.QtCore import QSize, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QStackedWidget, QFileDialog, QListWidgetItem, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QMessageBox, QListWidget, QPlainTextEdit
from PyQt5.uic import loadUi

from Gmail import DownloadEmail
from Steganography import ExtractFromVideo, ExtractFromImage


# Decryption Ui : it has three interfaces (Main Decryption , EmailStatus_Decryption ,ExtractEmailContent_Decryption)

class QCustomQWidget(QWidget):
    subject: str
    sender: str

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)

        self.textQHBoxLayout = QHBoxLayout()

        self.txtSubject = QLabel()
        self.txtSender = QLabel()
        self.txtSubject.setFixedHeight(50)
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
            color: rgb(0, 0, 0);
            background-color: rgba(0,0,0,0);
        ''')
        self.txtSender.setStyleSheet('''
            color: rgb(0, 0, 0);
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
    # testList = [("hi", "Taha"), ("Iloveshwarma", "Izzat"), ("what's up bro", "Fathi")]
    emailList = []

    def __init__(self, allWidgets):
        super(Decryption, self).__init__()
        loadUi("./UI_Files/Decryption.ui", self)

        self.allWidgets = allWidgets
        self.stackedWidget = allWidgets.widgets

        #self.btnUploadStego.clicked.connect(self.uploadFile)

        self.btnEmailStatus.clicked.connect(self.goToEmailStatus)

        self.btnEmailContent.clicked.connect(self.goToEmailContent)
        self.btnEncryption.clicked.connect(self.goToEncryption)
        self.btnStegoContent.clicked.connect(self.goToStegoContent)

        # self.lwEmails.itemClicked.connect(self.goToEmailStatusFromList)

        # self.fillList()
        self.lwEmails.itemClicked.connect(self.goToEmailStatusFromList)
        # QListWidget.

    def fillList(self):

        self.lwEmails.clear()
        for email in self.emailList:
            customListItem = QCustomQWidget()
            customListItem.setSubject(email[2])
            customListItem.setSender(email[1])

            myQListWidgetItem = QListWidgetItem(self.lwEmails)
            myQListWidgetItem.setSizeHint(customListItem.sizeHint())

            self.lwEmails.addItem(myQListWidgetItem)
            self.lwEmails.setItemWidget(myQListWidgetItem, customListItem)

    def goToEmailStatus(self):
        self.allWidgets.goToEmailStatus()

    def goToEmailStatusFromList(self, item: QListWidgetItem):

        customItem = self.lwEmails.itemWidget(item)
        itemIndex = self.lwEmails.row(item)

        print(customItem.getSubjectString() + "  " + customItem.getSenderString())

        self.allWidgets.goToEmailStatusFromList(customItem, itemIndex)

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

    seed: int
    key: str
    iv: str

    currentMailIndex: int

    def __init__(self, allWidgets):
        super(EmailStatus, self).__init__()
        loadUi("./UI_Files/Stego File Information.ui", self)

        self.allWidgets = allWidgets
        self.stackedWidget = allWidgets.widgets

        self.btnEncryption.clicked.connect(self.goToEncryption)
        self.btnStegoContent.clicked.connect(self.goToStegoContent)
        self.btnEmailContent.clicked.connect(self.goToEmailInformation)

        self.btnDecryption.clicked.connect(self.goToDecryption)
        self.btnExtract.clicked.connect(self.extractStegoFile)
        self.btnStegoMails.clicked.connect(self.goToDecryption)

    def goToDecryption(self):
        self.allWidgets.goToDecryption()

    def goToStegoContent(self):  # go to  Stego content UI
        self.allWidgets.goToStegoContent()

    def goToEncryption(self):  # go to  Gmail content UI
        self.allWidgets.goToEncryption()

    def goToEmailInformation(self):
        self.allWidgets.goToEmailInformation()

    def extractStegoFile(self):
        # filter = "Images (*.png *.bmp )"
        # outputDestination = QFileDialog.getOpenFileNames(self, 'Set Output Destination', '', filter=filter)
        fileDirectory = QFileDialog.getExistingDirectory(self, "Set Output Destination", './')

        if fileDirectory:
            messageIndex = self.allWidgets.widgetsObjects[12].currentMailIndex
            messageID = DownloadEmail.messageID[messageIndex]

            DownloadEmail.downloadAttachment(messageID)

            emailBody = DownloadEmail.bodies[messageIndex]

            self.seed = int(emailBody.split("|")[1])
            self.key = emailBody.split("|")[2].encode('utf-8')
            self.iv = emailBody.split("|")[3].encode('utf-8')

            self.stackedWidget.setCurrentIndex(13)
            self.allWidgets.widgetsObjects[13].extractStegoFile(fileDirectory,messageIndex)
            self.stackedWidget.setFixedSize(QSize(600, 400))


class ExtractStego(QDialog):
    stackedWidget: QStackedWidget

    cancelled = False
    paused = False

    def __init__(self, allWidgets):
        super(ExtractStego, self).__init__()
        loadUi("./UI_Files/Extracting Stego.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.allWidgets = allWidgets

        self.emailStatus = self.allWidgets.widgetsObjects[12]

        self.btnCancel.clicked.connect(self.cancelStegoMail)
        self.btnDone.clicked.connect(self.backToDecryption)


    def backToDecryption(self):
        self.allWidgets.goToDecryption()

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

        # print(QMessageBox.Yes)

    def extractStegoFile(self, fileDirectory,messageIndex):

        if DownloadEmail.attachmentNames[messageIndex].split(".")[-1] == "avi":
            self.extractMedia = ExtractFromVideo.ExtractFromVideo()
            t1 = threading.Thread(target=self.extractFromVideo, daemon=True,kwargs={"fileDirectory":fileDirectory,"messageIndex":messageIndex})
        else:
            self.extractMedia = ExtractFromImage.ExtractFromImage()
            t1 = threading.Thread(target=self.extractFromImage, daemon=True,kwargs={"fileDirectory":fileDirectory,"messageIndex":messageIndex})


        t1.start()

        self.startTheThread()

    def startTheThread(self):
        self.cancelled = False
        self.paused = False


        self.btnDone.hide()
        self.btnCancel.show()

        t = threading.Thread(daemon=True, name='StatusThread', target=UpdateUI,
                             args=[self.updateUI, self])
        t.start()

    def updateUI(self, progress):
        self.progressBar.setValue(progress)

        if progress == 100:
            self.btnDone.show()
            self.btnCancel.hide()

            self.txtStatus.setText("Status: Content Extracted Successfully")
        elif progress == 90:
            self.txtStatus.setText("Status: Validating Extracted Content")
        elif 40 == progress or progress == 80:
            self.txtStatus.setText("Status: Extracting Content")
        elif progress < 40:
            self.txtStatus.setText("Status: Preparing file for extracting")

        if  self.extractMedia.missingHeaderError:
            print("Missing Header Error")

        if  self.extractMedia.invalidSignatureError:
            print("Invalid Signature")

    def extractFromVideo(self, fileDirectory, messageIndex):
        self.extractMedia.extractFromVideo("./tempFiles/" + DownloadEmail.attachmentNames[messageIndex],
                                           fileDirectory + "/",
                                           self.emailStatus.seed,
                                           self.emailStatus.key,
                                           self.emailStatus.iv)

    def extractFromImage(self, fileDirectory, messageIndex):
        self.extractMedia.extractFromImage("./tempFiles/" + DownloadEmail.attachmentNames[messageIndex],
                                           fileDirectory + "/",
                                           self.emailStatus.seed,
                                           self.emailStatus.key,
                                           self.emailStatus.iv)

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


def UpdateUI(callbackFunc, retrievedMail):
    mySrc = Communicate()
    mySrc.myGUI_signal.connect(callbackFunc)

    while not retrievedMail.cancelled:
        while retrievedMail.paused:
            continue
        mySrc.myGUI_signal.emit(retrievedMail.extractMedia.progress)
        time.sleep(0.5)


    mySrc.myGUI_signal.emit(0)

    retrievedMail.allWidgets.RemoveTempFiles()
