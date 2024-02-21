from PIL import Image
from pyzbar.pyzbar import decode


#https://stackoverflow.com/a/52428362/17870878
#https://note.nkmk.me/en/python-pyzbar-barcode-qrcode/
def decodeQR(qrPath:str):
    data = decode(Image.open(qrPath))
    return data[0].data.decode('utf-8')