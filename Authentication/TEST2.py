import cv2


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