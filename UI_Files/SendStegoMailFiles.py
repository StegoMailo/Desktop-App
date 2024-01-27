import os
import random
import re
import threading
import time
from email.utils import parseaddr
from threading import Thread

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QStackedWidget, QMessageBox, QProgressBar
from PyQt5.uic import loadUi


# Encryption Ui : it has three interfaces (Main Encrypting , Advanced Settings ,Email Content)

class DraggableFilesQLabelSecretFile(QLabel):
    filePath = ""

    txtSecretFileSize: QLabel
    txtSecretFileName: QLabel
    txtFileSizeValidation: QLabel

    def __init__(self, widget, txtCoverMedia, sendStegoScreen: QDialog, txtSecretFileSize: QLabel,
                 txtSecretFileName: QLabel, txtFileSizeValidation: QLabel):
        super(DraggableFilesQLabelSecretFile, self).__init__(widget)

        self.setAcceptDrops(True)

        self.txtSecretFileName = txtSecretFileName
        self.txtSecretFileSize = txtSecretFileSize
        self.sendStegoScreen = sendStegoScreen

        self.txtCoverMedia = txtCoverMedia

        self.txtFileSizeValidation = txtFileSizeValidation

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().text()
        file_path = re.sub('file:///', '', file_path)
        self.filePath = file_path

        self.setPixmap(QPixmap(self.filePath))
        self.setScaledContents(True)

        # object1 = DraggableFiles_Cover_Media()

        secretFileSize = (float(os.path.getsize(file_path) / (1024 ** 2)))
        self.txtSecretFileSize.setText("Media size: " + f"{secretFileSize:.3f}" + "  MB")  # in bytes

        self.txtSecretFileName.setText("Secret File Name: " + os.path.basename(file_path))

        maxSecretSize = self.txtCoverMedia.maxSecretSize

        if maxSecretSize != 0:
            if maxSecretSize >= secretFileSize:
                self.txtFileSizeValidation.setText("File Can Be Sent")
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)

                msg.setText(
                    "There is not enough space in the Cover Media to hide the secret file!\nPlease choose a bigger cover media file or a smaller secret file")

                msg.setWindowTitle("Cannot Hide!")

                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()


class DraggableFilesQLabelCoverMedia(QLabel):
    secretFilePath: str

    fileNameLabel: QLabel
    fileSizeLabel: QLabel
    maxSecretMessageSizeLabel: QLabel

    maxSecretSize = 0

    def __init__(self, widget, fileNameLabel: QLabel, fileSizeLabel: QLabel, maxSecretMessageSizeLabel: QLabel):
        super(DraggableFilesQLabelCoverMedia, self).__init__(widget)

        self.setAcceptDrops(True)
        self.fileNameLabel = fileNameLabel
        self.fileSizeLabel = fileSizeLabel
        self.maxSecretMessageSizeLabel = maxSecretMessageSizeLabel

    def dragEnterEvent(self, event):
        file_name = event.mimeData().text()
        if file_name.split('.')[-1] in ['bmp', 'BMP', 'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'mp4', 'MP4']:
            event.acceptProposedAction()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText("Please only use an image or video!")

            msg.setWindowTitle("Invalid File Type")

            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

            event.ignore()

    def dropEvent(self, event):
        # print(event.mimeData().text())

        file_path = event.mimeData().text()
        self.secretFilePath = re.sub('file:///', '', file_path)
        print(file_path)

        if file_path.split('.')[-1] == "mp4":

            cap = cv2.VideoCapture(self.secretFilePath)

            allFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            random.seed(1)

            cap.set(cv2.CAP_PROP_POS_FRAMES, random.randint(0, allFrames - 1))

            ret, frame = cap.read()

            if ret:
                print("hi")
            else:
                print("not hi")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            self.setPixmap(QPixmap(img))
            self.setScaledContents(True)

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            colors = 3

            self.maxSecretSize = int(width * frames * height * colors) // 8

        else:

            image = cv2.imread(self.secretFilePath)

            width = len(image)
            height = len(image[0])
            print(width)
            print(height)
            colors = 3
            print("TEST")
            self.maxSecretSize = (int(width * height * colors) // 8) / (1024 ** 2)

            print(self.maxSecretSize)

            self.setPixmap(QPixmap(self.secretFilePath))
            self.setScaledContents(True)

        # Extract file name and size

        coverFileName = os.path.basename(self.secretFilePath)
        coverFileSize = float((os.path.getsize(self.secretFilePath)) / (1024 ** 2))

        if self.maxSecretSize > 5:
            self.maxSecretSize = 5

        self.fileNameLabel.setText("Media Name: " + coverFileName)
        self.fileSizeLabel.setText("Media Size: " + f"{coverFileSize:.3f}" + "  MB")  # in bytes
        self.maxSecretMessageSizeLabel.setText("Max Secret File:  " + f"{self.maxSecretSize:.3f}" + "  MB")


class Encryption(QDialog):
    stackedWidget: QStackedWidget

    secretFilePath: str
    coverMediaPath: str

    def __init__(self, allWidgets):
        super(Encryption, self).__init__()
        loadUi("Encryption.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.txtCoverBrowse.mousePressEvent = self.browseCoverMedia
        self.txtSecretFileBrowse.mousePressEvent = self.browseSecretFile

        self.btnEmailContent.clicked.connect(self.goToEmailInformation)
        self.btnContinue.clicked.connect(self.goToEmailInformation)

        self.btnAdvancedSettings.clicked.connect(self.goToAdvancedSettings)

        self.btnDecryption.clicked.connect(self.goToDecryption)
        self.btnEmailStatus.clicked.connect(self.goToEmailStatus)

        self.txtCoverMediaArea = DraggableFilesQLabelCoverMedia(self, self.txtMediaName, self.txtMediaSize,
                                                                self.txtMaxSecretMessageSize)

        self.txtSecretFileArea = DraggableFilesQLabelSecretFile(self, self.txtCoverMediaArea, self, self.txtSecretName
                                                                , self.txtSecretSize, self.txtFileSizeValidation)

        self.txtCoverMediaArea.setGeometry(340, 220, 251, 221)  # x,y width,height

        self.txtCoverMediaArea.setStyleSheet(
            "background-color: rgba(138, 198, 253,0.5);   border-radius:10px; border: 0.5px solid #000000;"
            " color: rgb(0,0,0);")

        tempFont = self.txtCoverMediaArea.font()
        tempFont.setBold(True)
        tempFont.setPointSize(16)

        self.txtCoverMediaArea.setFont(tempFont)
        self.txtCoverMediaArea.setText("Drop Cover\nMedia Here")
        self.txtCoverMediaArea.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.txtSecretFileArea.setGeometry(850, 220, 251, 221)  # x,y width,height

        self.txtSecretFileArea.setStyleSheet(
            "background-color: rgba(138, 198, 253,0.5); border-radius:10px; border: 0.5px solid #000000;"
            " color: rgb(0,0,0);")

        tempFont = self.txtSecretFileArea.font()
        tempFont.setBold(True)
        tempFont.setPointSize(16)
        self.txtSecretFileArea.setFont(tempFont)

        self.txtSecretFileArea.setText("Drop Secret\nFile Here")
        self.txtSecretFileArea.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.txtCoverBrowse.raise_()
        self.txtSecretFileBrowse.raise_()

    def browseCoverMedia(self, *arg, **kwargs):
        filter = "Videos (.mp4), Images(*.png , *.jpg , *.jpeg , *.bmp)"
        messageFileName = QFileDialog.getOpenFileNames(self, 'Get Message File', './', filter=filter)

        if len(messageFileName[0]) != 0:
            self.txtFileChosen.setText(messageFileName[0][0].split("/")[-1])

            filePath = messageFileName[0][0]
            coverFileName = os.path.basename(filePath)
            coverFileSize = float((os.path.getsize(filePath)) / 1024)
            self.maxSecretSize = (float((os.path.getsize(filePath) / 8) / 1024))

            if self.maxSecretSize > 25:
                self.maxSecretSize = 25

            self.fileNameLabel.setText("Media Name: " + coverFileName)
            self.fileSizeLabel.setText("Media Size: " + f"{coverFileSize:.3f}" + "  MB")  # in bytes
            self.maxSecretMessageSizeLabel.setText("Max Secret File:  " + f"{self.maxSecretSize:.3f}" + "  MB")

    def browseSecretFile(self, *arg, **kwargs):
        messageFileName = QFileDialog.getOpenFileNames(self, 'Get Message File', './')

        if len(messageFileName[0]) != 0:
            self.txtMediaName.setText(messageFileName[0][0].split("/")[-1])

    def on_send_stego_file_clicked(self):
        print("Send Stego File button clicked!")

    def goToAdvancedSettings(self):
        self.stackedWidget.setCurrentIndex(8)
        self.stackedWidget.setFixedSize(QSize(670, 601))

    # stegoEmail_Information
    def goToEmailInformation(self):
        self.stackedWidget.setCurrentIndex(9)
        self.stackedWidget.setFixedSize(QSize(1081, 711))

    # Decryption_pushButton
    def goToDecryption(self):
        # createacc = Decryption()
        # self.stackedWidget.addWidget(createacc)
        # self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        print("To Decryption")

    def goToEmailStatus(self):
        # createacc = EmailStatus_Decryption()
        # self.stackedWidget.addWidget(createacc)
        # self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        print("To Decryption")


class AdvancedSettings(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(AdvancedSettings, self).__init__()
        loadUi("Advanced Settings.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.btnDone.clicked.connect(self.goToEncryption)

    def goToEncryption(self):  # get data then     backToEncryptionUI
        EncryptionKey = self.tfKey.text()
        seed = self.tfSeed.text()
        isSoundUsed = self.chkSound.isChecked()
        saveStegoMedia = self.chkSave.isChecked()

        print(EncryptionKey)
        print(seed)
        print(isSoundUsed)
        print(saveStegoMedia)

        self.stackedWidget.setCurrentIndex(7)
        self.stackedWidget.setFixedSize(QSize(1223, 685))


class EmailInformation(QDialog):
    stackedWidget: QStackedWidget


    def __init__(self, allWidgets):
        super(EmailInformation, self).__init__()
        loadUi("Email Information.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.allWidgets = allWidgets

        # self.Decryption_pushButton.clicked.connect(self.on_Decryption_pushButton_clicked)
        # self.EmailStatusButton.clicked.connect(self.on_EmailStatus_pushButton_clicked)
        # self.stegoContentButton.clicked.connect(self.on_stegoEmail_Information_clicked)

        self.btnSend.clicked.connect(self.sendStegoMail)

    def sendStegoMail(self):  # send the Email content then backToEncryptionUI
        receiver = self.tfTo.text()
        emailSubject = self.tfSubject.text()
        bodyEmail = self.tfBody.toPlainText()

        if len(receiver) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText(
                "The email's address is empty!\nPlease enter an email address for this email.")

            msg.setWindowTitle("Empty Email!")

            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", receiver):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)

                msg.setText(
                    "The email you have entered is invalid!\nPlease enter a valid email address.")

                msg.setWindowTitle("Invalid Email!")

                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()
            else:
                if len(emailSubject) == 0:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)

                    msg.setText(
                        "The email's subject is empty!\nPlease enter a subject for this email.")

                    msg.setWindowTitle("Empty Subject!")

                    msg.setStandardButtons(QMessageBox.Ok)
                    retval = msg.exec_()
                else:
                    print(receiver)
                    print(emailSubject)
                    print(bodyEmail)
                    print("Send the stego mail")

                    self.stackedWidget.setCurrentIndex(10)
                    self.allWidgets.widgetsObjects[10].encodeStegoFile()
                    self.stackedWidget.setFixedSize(QSize(600, 400))

    def on_Decryption_pushButton_clicked(self):
        # createacc = Decryption()
        # self.stackedWidget.addWidget(createacc)
        # self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        print("To Decryption")

    def on_EmailStatus_pushButton_clicked(self):
        # createacc = EmailStatus_Decryption()
        # self.stackedWidget.addWidget(createacc)
        # self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        print("To Decryption")

        # stegoEmail_Information

    def on_stegoEmail_Information_clicked(self):
        createacc = Encryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)


class SentEmailStatus(QDialog):
    stackedWidget: QStackedWidget

    cancelled = False

    def __init__(self, allWidgets):
        super(SentEmailStatus, self).__init__()
        loadUi("Send Email.ui", self)

        self.stackedWidget = allWidgets.widgets

        self.btnCancel.clicked.connect(self.changeCancelValue)

    def changeCancelValue(self):
        self.cancelled=True
    def encodeStegoFile(self):
        progress = 0
        t1 = Thread(target=self.count, daemon=True, kwargs={'progress': progress})
        t1.start()

        self.startTheThread(self)

    def startTheThread(self, progress):
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
        time.sleep(1)
        progress += 1
        mySrc.myGUI_signal.emit(progress)
