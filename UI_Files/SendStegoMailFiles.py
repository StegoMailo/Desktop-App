import os
import random
import re
import threading
import time
from threading import Thread

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QStackedWidget, QMessageBox
from PyQt5.uic import loadUi


# Encryption Ui : it has three interfaces (Main Encrypting , Advanced Settings ,Gmail Content)

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
        self.txtSecretFileName.setText("Secret File Size: " + f"{secretFileSize:.3f}" + "  MB")  # in bytes

        self.txtSecretFileSize.setText("Secret File Name: " + os.path.basename(file_path))

        maxSecretSize = self.txtCoverMedia.maxSecretSize

        if maxSecretSize != 0:
            if maxSecretSize >= secretFileSize:
                self.txtFileSizeValidation.setText("File Can Be Sent")
                self.sendStegoScreen.allWidgets.secretFilePath = file_path
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

    def __init__(self, widget, sendStegoScreen: QDialog, fileNameLabel: QLabel, fileSizeLabel: QLabel,
                 maxSecretMessageSizeLabel: QLabel):
        super(DraggableFilesQLabelCoverMedia, self).__init__(widget)

        self.sendStegoScreen = sendStegoScreen

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

        self.sendStegoScreen.allWidgets.coverMediaPath = file_path


class Encryption(QDialog):
    stackedWidget: QStackedWidget

    secretFilePath: str
    coverMediaPath: str

    def __init__(self, allWidgets):
        super(Encryption, self).__init__()
        loadUi("./UI_Files/Encryption.ui", self)

        self.allWidgets = allWidgets
        self.stackedWidget = allWidgets.widgets
        self.txtCoverBrowse.mousePressEvent = self.browseCoverMedia
        self.txtSecretFileBrowse.mousePressEvent = self.browseSecretFile

        self.btnEmailContent.clicked.connect(self.goToEmailInformation)
        self.btnContinue.clicked.connect(self.goToEmailInformation)

        self.btnAdvancedSettings.clicked.connect(self.goToAdvancedSettings)

        self.btnDecryption.clicked.connect(self.goToDecryption)
        self.btnEmailStatus.clicked.connect(self.goToEmailStatus)

        self.txtCoverMediaArea = DraggableFilesQLabelCoverMedia(self,self, self.txtMediaName, self.txtMediaSize,
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

        self.btnStegoMails.clicked.connect(self.goToDecryption)

    def goToDecryption(self):
        self.allWidgets.goToDecryption()

    def browseCoverMedia(self, *arg, **kwargs):
        filter = "Videos (.mp4), Images(*.png , *.jpg , *.jpeg , *.bmp)"
        coverFilePath = QFileDialog.getOpenFileNames(self, 'Get Message File', './', filter=filter)

        if len(coverFilePath[0]) != 0:

            file_path = coverFilePath[0][0]

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
                self.txtCoverMediaArea.setPixmap(QPixmap(img))
                self.txtCoverMediaArea.setScaledContents(True)

                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                colors = 3

                self.maxSecretSize = int(width * frames * height * colors) // 8

            else:

                image = cv2.imread(file_path)

                width = len(image)
                height = len(image[0])
                print(width)
                print(height)
                colors = 3
                print("TEST")
                self.maxSecretSize = (int(width * height * colors) // 8) / (1024 ** 2)

                print(self.maxSecretSize)

                self.txtCoverMediaArea.setPixmap(QPixmap(file_path))
                self.txtCoverMediaArea.setScaledContents(True)

            # Extract file name and size

            coverFileName = os.path.basename(file_path)
            coverFileSize = float((os.path.getsize(file_path)) / (1024 ** 2))

            if self.maxSecretSize > 5:
                self.maxSecretSize = 5

            self.txtMediaName.setText("Media Name: " + coverFileName)
            self.txtMediaSize.setText("Media Size: " + f"{coverFileSize:.3f}" + "  MB")  # in bytes
            self.txtMaxSecretMessageSize.setText("Max Secret File:  " + f"{self.maxSecretSize:.3f}" + "  MB")

    def browseSecretFile(self, *arg, **kwargs):
        messageFileName = QFileDialog.getOpenFileNames(self, 'Get Message File', './')

        if len(messageFileName[0]) != 0:
            file_path = messageFileName[0][0]

            #self.setPixmap(QPixmap(file_path))
            #self.setScaledContents(True)

            # object1 = DraggableFiles_Cover_Media()

            secretFileSize = (float(os.path.getsize(file_path) / (1024 ** 2)))
            self.txtSecretSize.setText("Secret File Size: " + f"{secretFileSize:.3f}" + "  MB")  # in bytes

            self.txtSecretName.setText("Secret File Name: " + os.path.basename(file_path))

            maxSecretSize = self.txtCoverMediaArea.maxSecretSize

            if maxSecretSize != 0:
                if maxSecretSize >= secretFileSize:
                    self.txtFileSizeValidation.setText("File Can Be Sent")
                    self.allWidgets.secretFilePath = file_path
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)

                    msg.setText(
                        "There is not enough space in the Cover Media to hide the secret file!\nPlease choose a bigger cover media file or a smaller secret file")

                    msg.setWindowTitle("Cannot Hide!")

                    msg.setStandardButtons(QMessageBox.Ok)
                    retval = msg.exec_()

    def goToAdvancedSettings(self):
        self.stackedWidget.setCurrentIndex(8)
        self.stackedWidget.setFixedSize(QSize(670, 601))

    def goToEmailInformation(self):
        self.allWidgets.goToEmailInformation()

    def goToEmailStatus(self):
        self.allWidgets.goToEmailStatus()


class AdvancedSettings(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(AdvancedSettings, self).__init__()
        loadUi("./UI_Files/Advanced Settings.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.allWidgets = allWidgets
        self.btnDone.clicked.connect(self.goToEncryption)

    def goToEncryption(self):  # get data then     backToEncryptionUI

        self.allWidgets.EncryptionKey = self.tfKey.text()
        self.allWidgets.seed = self.tfSeed.text()
        self.allWidgets.isSoundUsed = self.chkSound.isChecked()
        self.allWidgets.saveStegoMedia = self.chkSave.isChecked()

        print(self.allWidgets.EncryptionKey)
        print(self.allWidgets.seed)
        print(self.allWidgets.isSoundUsed)
        print(self.allWidgets.saveStegoMedia)

        self.stackedWidget.setCurrentIndex(7)
        self.stackedWidget.setFixedSize(QSize(1223, 682))


class EmailInformation(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self, allWidgets):
        super(EmailInformation, self).__init__()
        loadUi("./UI_Files/Email Information.ui", self)

        self.stackedWidget = allWidgets.widgets
        self.allWidgets = allWidgets

        self.btnEncryption.clicked.connect(self.goToStegoContent)

        self.btnDecryption.clicked.connect(self.goToDecryption)
        self.btnEmailStatus.clicked.connect(self.goToEmailStatus)
        self.btnStegoContent.clicked.connect(self.goToStegoContent)

        self.btnSend.clicked.connect(self.sendStegoMail)

        self.btnStegoMails.clicked.connect(self.goToDecryption)

    def goToDecryption(self):
        self.allWidgets.goToDecryption()

    def sendStegoMail(self):  # send the Gmail content then backToEncryptionUI
        receiver = self.tfTo.text()
        emailSubject = self.tfSubject.text()
        bodyEmail = self.tfBody.toPlainText()

        if len(receiver) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText(
                "The email's address is empty!\nPlease enter an email address for this email.")

            msg.setWindowTitle("Empty Gmail!")

            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", receiver):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)

                msg.setText(
                    "The email you have entered is invalid!\nPlease enter a valid email address.")

                msg.setWindowTitle("Invalid Gmail!")

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

    def goToDecryption(self):
        self.allWidgets.goToDecryption()

    def goToEmailStatus(self):
        self.allWidgets.goToEmailStatus()

    def goToStegoContent(self):
        self.allWidgets.goToStegoContent()


class SentEmailStatus(QDialog):
    stackedWidget: QStackedWidget

    cancelled = False
    paused = False

    def __init__(self, allWidgets):
        super(SentEmailStatus, self).__init__()
        loadUi("./UI_Files/Send Email.ui", self)

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
        t1 = Thread(target=self.count, daemon=True, kwargs={'progress': progress})
        t1.start()

        self.startTheThread(self)

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
        time.sleep(1)
        progress += 1
        mySrc.myGUI_signal.emit(progress)
    mySrc.myGUI_signal.emit(0)
