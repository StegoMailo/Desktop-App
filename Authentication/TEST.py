import io
import random
import string

import qrcode


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=13, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


data = ''.join(random.choice(string.ascii_letters) for _ in range(25))