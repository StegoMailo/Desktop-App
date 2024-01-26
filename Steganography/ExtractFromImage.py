import os

import cv2
import random
import math
from hashlib import sha256
from Cipher.AES import AESCipher
from base64 import b64decode


class ExtractFromImage():

    # Function to convert a binary in string representation to integer
    def BinaryStringToInteger(self, BinaryString):
        return int(BinaryString, 2)

    def extractFromImage(self, watermarkedImagePath, outputDestination, seed, key, iv):

        WatermarkedImage = cv2.imread(watermarkedImagePath)
        WatermarkedImage = cv2.cvtColor(WatermarkedImage, cv2.COLOR_BGR2RGB)

        # Generate random sequence to extract Logo Information

        # First, the first 800 bits will be extracted
        # 800 bits should be enough to represent both the file name and file size

        random.seed(seed)

        points = random.sample([[x, y] for x in range(len(WatermarkedImage)) for y in range(len(WatermarkedImage[0]))],
                               math.floor(800 / 3) + 1)

        # Extract the bit stream of the logo information

        # First, the first 800 bits will be extracted
        # 800 bits should be enough to represent both the file name and file size

        LogoInformationBinary = []

        LogoInformationLength = 800

        i = 0
        for point in points:
            for color in range(len(WatermarkedImage[point[0]][point[1]])):
                if i == LogoInformationLength:
                    break

                bit = WatermarkedImage[point[0]][point[1]][color] & 1
                LogoInformationBinary.append(str(bit))
                i += 1
            else:
                continue

        # Convert the logo information to groups of 8 bits

        LogoInformationBinaryList = []
        BinaryString = ""

        i = 0
        for bit in LogoInformationBinary:

            BinaryString += bit
            i += 1

            if i > 7:
                LogoInformationBinaryList.append(BinaryString)
                BinaryString = ""
                i = 0

        # Convert logo information bit stream to integer

        LogoInformationAscii = []

        for BinaryString in LogoInformationBinaryList:
            LogoInformationAscii.append(self.BinaryStringToInteger(BinaryString))

        # Convert logo information integer to String

        LogoInformation = ""

        for letter in LogoInformationAscii:
            LogoInformation += chr(letter)

        # Extract the important information

        logoInformationSplit = LogoInformation.split('|')

        if len(logoInformationSplit) != 4 and not logoInformationSplit[
            0].isnumeric():  # works because i think if the first part is false the rest isn't checked
            print("File Does Not Contain Any Hidden Information!")
            return

        logoInformationSize = (len(logoInformationSplit[0]) + len(logoInformationSplit[1]) + len(
            logoInformationSplit[2]) + 3) * 8

        fileSize = int(logoInformationSplit[0])
        fileName = logoInformationSplit[1]
        fileHash = logoInformationSplit[2]
        # Generate pixel extractions sequence for the logo using the logo information

        random.seed(seed)

        LogoLength = fileSize

        points2 = random.sample([[x, y] for x in range(len(WatermarkedImage)) for y in range(len(WatermarkedImage[0]))],
                                math.ceil((LogoLength + logoInformationSize) / 3))

        # Extract the logo from the image, results in a list of integers

        LogoBinary = []

        i = 0
        for point in points2:
            for color in range(len(WatermarkedImage[point[0]][point[1]])):
                if i > logoInformationSize - 1:
                    if i == LogoLength + logoInformationSize:
                        break

                    bit = WatermarkedImage[point[0]][point[1]][color] & 1
                    LogoBinary.append(str(bit))
                i += 1

            else:
                continue

        LogoBinaryList = []
        BinaryString = ""

        i = 0
        for bit in LogoBinary:

            BinaryString += bit
            i += 1

            if i > 7:
                LogoBinaryList.append(BinaryString)
                BinaryString = ""
                i = 0

        generatedHash = sha256("".join(LogoBinaryList).encode('utf-8')).hexdigest()

        if generatedHash != fileHash:
            print("File Was Not Extracted Correctly!")
        else:
            print("Extracted Successfully!")

        LogoAscii = []

        for BinaryString in LogoBinaryList:
            LogoAscii.append(self.BinaryStringToInteger(BinaryString))

        # Convert the list of integers to  bytestream

        LogoByteStream = bytes(LogoAscii)

        #Decrypt the ciphertext
        LogoByteStream = AESCipher().decrypt(LogoByteStream, key, iv)

        # Write file as bytes
        # if not os.path.exists("./Extracted Files"):
        #     os.makedirs("Extracted Files")

        with open(outputDestination + fileName, 'wb') as f:
            f.write(LogoByteStream)
