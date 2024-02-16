import io
import random
import string

import qrcode
import sys

from PIL import ImageQt
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=13, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10

        # Load the UI file
        uic.loadUi("QrCodeui.ui", self)

        # Create a QLabel to display the QR code
        self.browseButton.clicked.connect(self.browse)
        self.saveButton.clicked.connect(self.save)
        self.homeButton.clicked.connect(self.home)
        self.show()
        self.saveButton.hide()
        self.saveWarning.hide()

    def browse(self):
        #TODO IZZAT "Check QR code with database"
        data = ''.join(random.choice(string.ascii_letters) for _ in range(25))
        print(data)
        # Update the QLabel with the new QPixmap
        image = generate_qr_code(data)

        pixmap = QPixmap()
        pixmap.loadFromData(image)

        self.imageLabel.setPixmap(pixmap)
        self.saveButton.show()
        self.saveWarning.show()
        self.browseButton.hide()
        self.imageLabel.show()

    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)",
                                                  options=options)
        if filePath:
            # Save the image to the specified file path with the filename 'qr.png'
            # Ensure the file has the '.png' extension
            if not filePath.lower().endswith('.png'):
                filePath += '.png'
            self.imageLabel.pixmap().save(filePath, 'png')
            self.browseButton.show()

            self.saveButton.hide()

            self.imageLabel.clear()

    def home(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
