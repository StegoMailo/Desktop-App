##########################################################################################################
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QStackedWidget, QFileDialog, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QFrame
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
        # setStyleSheet





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
    stackedWidget: QStackedWidget
    testList = [("hi", "Taha"), ("Iloveshwarma", "Izzat"), ("what's up bro", "Fathi")]

    def __init__(self, allWidgets):
        super(Decryption, self).__init__()
        loadUi("Decryption.ui", self)

        self.stackedWidget = allWidgets.widgets

        self.UploadEncryptedMedia_pushButton.clicked.connect(self.choose_file)
        self.EmailStatus_pushButton.clicked.connect(self.goToEmailFromCustomFile)
        self.emailContentButton.clicked.connect(self.on_emailContentButton_clicked)
        self.encryption_Button.clicked.connect(self.on_emailContentButton_clicked)
        self.stegoContentButton.clicked.connect(self.on_stegoEmail_Information_clicked)

        #self.lwEmails.itemClicked.connect(self.goToEmailStatusFromList)


        self.fillList()
        self.lwEmails.itemClicked.connect(self.goToEmailStatusFromList)
        #QListWidget.

    def fillList(self):
        for subject, sender in self.testList:
            customListItem = QCustomQWidget()
            customListItem.setSubject(subject)
            customListItem.setSender(sender)


            myQListWidgetItem = QListWidgetItem(self.lwEmails)
            myQListWidgetItem.setSizeHint(customListItem.sizeHint())


            self.lwEmails.addItem(myQListWidgetItem)
            self.lwEmails.setItemWidget(myQListWidgetItem, customListItem)


    def goToEmailFromCustomFile(self):
        print("hi")

    def goToEmailStatusFromList(self, item:QListWidgetItem):

        customItem = self.lwEmails.itemWidget(item)

        print(customItem.getSubjectString()+"  "+customItem.getSenderString())

    def on_emailContentButton_clicked(self):  # go to  Email content UI
        # create = Encryption()
        # self.stackedWidget.addWidget(create)
        # self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)
        print("Go To Encryption")

    def on_stegoEmail_Information_clicked(self):
        # createacc = stegoEmail_Information()
        # self.stackedWidget.addWidget(createacc)
        # self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)
        print("Go To Encryption")

    def choose_file(self):
        # Open a file dialog to choose a file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)  # Allow selecting an existing file
        file_path, _ = file_dialog.getOpenFileName(self, 'Choose a file', '', 'All Files (*);;Text Files (*.txt)')

        if file_path:
            print(f'Selected File: {file_path}')


class EmailStatus_Decryption(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self):
        super(EmailStatus_Decryption, self).__init__()
        loadUi("deskTopUI\\EmailStatus_Decryption.ui", self)
        self.emailContentButton.clicked.connect(self.on_emailContentButton_clicked)
        self.encryption_Button.clicked.connect(self.on_emailContentButton_clicked)
        self.Decryption_pushButton.clicked.connect(self.on_Decryption_pushButton_clicked)
        self.stegoContentButton.clicked.connect(self.on_stegoEmail_Information_clicked)
        self.extractingEmailContent_Button.clicked.connect(self.on_extractingEmailContent_Button_clicked)

    def on_emailContentButton_clicked(self):  # go to  Email content UI
        # create = Encryption()
        # self.stackedWidget.addWidget(create)
        # self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)
        print("Go To Encryption")

    def on_Decryption_pushButton_clicked(self):
        createacc = Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)

    def on_stegoEmail_Information_clicked(self):
        # createacc = stegoEmail_Information()
        # self.stackedWidget.addWidget(createacc)
        # self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)
        print("Go To Encryption")

    def on_extractingEmailContent_Button_clicked(self):
        createacc = ExtractEmailContent_Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)


class ExtractEmailContent_Decryption(QDialog):
    stackedWidget: QStackedWidget

    def __init__(self):
        super(ExtractEmailContent_Decryption, self).__init__()
        loadUi("deskTopUI\\ExtractEmailContent_Decryption.ui", self)
        self.cancel_Button.clicked.connect(self.on_EmailStatus_pushButton_clicked)

    def on_EmailStatus_pushButton_clicked(self):
        createacc = EmailStatus_Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
