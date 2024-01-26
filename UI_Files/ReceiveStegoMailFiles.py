##########################################################################################################
from PyQt5.QtWidgets import QDialog, QStackedWidget, QFileDialog
from PyQt5.uic import loadUi


# Decryption Ui : it has three interfaces (Main Decryption , EmailStatus_Decryption ,ExtractEmailContent_Decryption)

class Decryption(QDialog):
    stackedWidget: QStackedWidget
    def __init__(self):
        super(Decryption, self).__init__()
        loadUi("Decryption.ui", self)

        self.UploadEncryptedMedia_pushButton.clicked.connect(self.choose_file)
        self.EmailStatus_pushButton.clicked.connect(self.on_EmailStatus_pushButton_clicked)
        self.emailContentButton.clicked.connect(self.on_emailContentButton_clicked)
        self.encryption_Button.clicked.connect(self.on_emailContentButton_clicked)
        self.stegoContentButton.clicked.connect(self.on_stegoEmail_Information_clicked)

    def on_EmailStatus_pushButton_clicked(self):
        createacc = EmailStatus_Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)

    def on_emailContentButton_clicked(self):  # go to  Email content UI
        create = Encryption()
        self.stackedWidget.addWidget(create)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)

    def on_stegoEmail_Information_clicked(self):
        createacc = stegoEmail_Information()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)

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
        create = Encryption()
        self.stackedWidget.addWidget(create)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)

    def on_Decryption_pushButton_clicked(self):
        createacc = Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)

    def on_stegoEmail_Information_clicked(self):
        createacc = stegoEmail_Information()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)

    def on_extractingEmailContent_Button_clicked(self):
        createacc = ExtractEmailContent_Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)


class ExtractEmailContent_Decryption(QDialog):
    stackedWidget: QStackedWidget
    def __init__(self):
        super(ExtractEmailContent_Decryption, self).__init__()
        loadUi("deskTopUI\\ExtractEmailContent_Decryption.ui", self)
        self.cancel_Button.clicked.connect(self.on_EmailStatus_pushButton_clicked)

    def on_EmailStatus_pushButton_clicked(self):
        createacc = EmailStatus_Decryption()
        self.stackedWidget.addWidget(createacc)
        self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex() + 1)
