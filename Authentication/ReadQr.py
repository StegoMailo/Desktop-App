import io
import cv2
from pyzbar.pyzbar import decode
import qrcode
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
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
        # Load the UI file
        uic.loadUi("ReadQR.ui", self)
        self.uploadButton.clicked.connect(self.choose_image)
        self.errorLabel.hide()
        self.show()

    def read_qr_code(self, image_path):
        try:
            # Read the image using OpenCV
            image = cv2.imread(image_path)

            if image is None:
                self.errorLabel.show()
                print("Error: Unable to read the image.")
                return

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Use the ZBar library to decode QR codes
            decoded_objects = decode(gray)

            # Loop through the decoded objects and print the data
            for obj in decoded_objects:
                data = obj.data.decode("utf-8")
                print(f"QR Code data: {data}")

            # Wait for a key press (0 means wait indefinitely)
            cv2.waitKey(0)

        except Exception as e:
            self.errorLabel.hide()
            print(f"An error occurred: {e}")

        finally:
            # Close the OpenCV window
            cv2.destroyAllWindows()

    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Choose Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=options)
        if file_path:
            self.read_qr_code(file_path)  # Call the method using 'self'


    def home(self):
        #Todo IZZAT "Go back to home page"
        self.close()

    def upload(self):
        #Todo IZZAT "move to encryption page"
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
