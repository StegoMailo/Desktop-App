import cv2
from PIL import Image
import random
import math

from hashlib import sha256
from Cipher.AES import AESCipher


class HideInImage():
    coverImageSize = 0

    def IntegerToBinaryString(self, number):
        return '{0:08b}'.format(number)

    def hideInImage(self, coverImageFileName, watermarkFileName, outputFileName, seed=-1):
        # Load Cover Image using OpenCV

        coverImage = cv2.imread(coverImageFileName)
        coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)

        self.coverImageSize = len(coverImage) * len(coverImage[0]) * 3  # In Bytes

        # Load Watermark to Hide
        with open(watermarkFileName, 'rb') as fp:#watermark = secret
            watermarkByteStream = fp.read()

        maxLogoSize = self.coverImageSize  # But in bits

        watermarkByteStream, key, iv = AESCipher().encrypt(watermarkByteStream)
        # Convert Bytestream to Binary

        watermarkAsBinaryString = ""

        for byte in watermarkByteStream:
            watermarkAsBinaryString += self.IntegerToBinaryString(byte)

        # Convert Important Information to Bit stream

        watermarkBitStreamSize = len(watermarkAsBinaryString)
        fileHash = sha256(watermarkAsBinaryString.encode('utf-8')).hexdigest()
        watermarkInformationToHide = str(watermarkBitStreamSize) + "|" + watermarkFileName + "|" + fileHash + "|"

        informationAsAscii = []

        for letter in watermarkInformationToHide:
            informationAsAscii.extend(ord(num) for num in letter)

        watermarkInformationBitStream = []

        for num in informationAsAscii:
            watermarkInformationBitStream.append(self.IntegerToBinaryString(num))

        watermarkInformationBitStreamString = "".join(watermarkInformationBitStream)

        # Combine the Information Bit stream with Watermark Bit stream

        informationToHide = watermarkInformationBitStreamString + watermarkAsBinaryString

        # See if the Logo fits

        if len(informationToHide) > maxLogoSize - 10:
            print("Logo is too big for this cover image")
            return
        # Generate Random Sequence to Hide in the Photo

        if seed == -1:
            seed = random.randint(0,
                                  9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
        random.seed(seed)

        points = random.sample([[x, y] for x in range(len(coverImage)) for y in range(len(coverImage[0]))],
                               math.ceil(len(informationToHide) / 3))

        # Hide the Watermark Bit stream in the pixels
        
        i = 0

        for point in points:
            for color in range(len(coverImage[point[0]][point[1]])):
                if i == len(informationToHide):
                    break

                if informationToHide[i] == '1':
                    coverImage[point[0]][point[1]][color] |= 1
                else:
                    coverImage[point[0]][point[1]][color] &= ~1

                i += 1
            else:
                continue

        # Save the Watermarked Image

        im = Image.fromarray(coverImage.astype('uint8')).convert('RGB')

        im.save(outputFileName)

        return seed, key, iv
