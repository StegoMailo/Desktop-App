import math
import random
from hashlib import sha256

import cv2

from Cipher.AES import AESCipher


class ExtractFromVideo():
    progress: int

    missingHeaderError: bool
    invalidSignatureError: bool

    def extractFromVideo(self, stegoVideoPath, extractPath, originalSeed, key, iv):

        self.progress = 0
        self.invalidSignatureError = False
        self.missingHeaderError = False

        stegoVideo = cv2.VideoCapture(stegoVideoPath)

        numberOfFrames = int(stegoVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(stegoVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(stegoVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        colorChannels = 3

        maxInformationHiddenPerFrame = int((height * width * colorChannels))

        # Extract Header
        seed = originalSeed
        random.seed(seed)

        # Generate Random Frame Access
        randomFrameAccess = random.sample(range(numberOfFrames), numberOfFrames)

        informationToExtractCounter = 1000
        numberOfBitsExtracted = 0
        extractedBits = []

        self.progress = 10

        # Iterate Video through the random frames
        for frameNumber in randomFrameAccess:
            # Select the random frame
            stegoVideo.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
            res, frame = stegoVideo.read()
            # Check to see if the frame is readable
            if not res:
                print("Video Contains Bad Frame")
                break
            else:
                # change the seed and generate random pixel points in the frame to extract bits from
                seed += 361
                random.seed(seed)
                # (math.ceil()/3) is done because the pixel is chosen randomly, not the color channel
                randomPixelPointsToExtractFrom = random.sample(
                    [[x, y] for x in range(len(frame)) for y in range(len(frame[0]))],
                    math.ceil(maxInformationHiddenPerFrame / 3))
                # Start Hiding in the frames
                for point in randomPixelPointsToExtractFrom:
                    # Move through the Colors in each pixel
                    for color in range(len(frame[point[0]][point[1]])):
                        # When all the bits are hidden break
                        if numberOfBitsExtracted == informationToExtractCounter:
                            print("Finished Extracting Header")
                            break
                        extractedBit = frame[point[0]][point[1]][color] & 1
                        extractedBits.append(str(extractedBit))
                        numberOfBitsExtracted += 1

                    else:
                        continue
                    break  # If break then break out of entire loop
                else:
                    continue
                break  # same here

        self.progress = 20

        HiddenMessageInformationBinaryList = []
        BinaryString = ""

        i = 0
        for bit in extractedBits:

            BinaryString += bit
            i += 1

            if i > 7:
                HiddenMessageInformationBinaryList.append(BinaryString)
                BinaryString = ""
                i = 0

        def BinaryStringToInteger(BinaryString):
            return int(BinaryString, 2)

        HiddenMessageInformationAscii = []

        for BinaryString in HiddenMessageInformationBinaryList:
            HiddenMessageInformationAscii.append(BinaryStringToInteger(BinaryString))

        HiddenMessageInformation = ""

        for letter in HiddenMessageInformationAscii:
            HiddenMessageInformation += chr(letter)

        # Hidden File Information
        print(HiddenMessageInformation)
        hiddenFileInformation = HiddenMessageInformation.split("|")

        hiddenFileBitSize = int(hiddenFileInformation[0])
        hiddenFileSignature = hiddenFileInformation[1]
        hiddenFileName = hiddenFileInformation[2]

        hiddenMessageInfromationSize = (len(hiddenFileInformation[0]) + len(hiddenFileInformation[1]) + len(
            hiddenFileInformation[2]) + 3) * 8

        self.progress = 30

        if len(hiddenFileInformation) != 4 and not hiddenFileInformation[
            0].isnumeric():  # works because I think if the first part is false the rest isn't checked
            self.missingHeaderError = True
            print("File Does Not Contain Any Hidden Information!")
            return

        # Extract File Bit Stream
        seed = originalSeed
        random.seed(seed)

        # Generate Random Frame Access
        randomFrameAccess = random.sample(range(numberOfFrames), numberOfFrames)

        totalBitsRead = 0
        numberOfBitsExtracted = 0
        hiddenFileExtractedBits = ""

        # Iterate Video through the random frames
        for frameNumber in randomFrameAccess:
            # Select the random frame
            stegoVideo.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
            res, frame = stegoVideo.read()
            # Check to see if the frame is readable
            if not res:
                print("Video Contains Bad Frame")
                break
            else:
                # change the seed and generate random pixel points in the frame to extract bits from
                seed += 361
                random.seed(seed)
                # (math.floor()/3) is done because the pixel is chosen randomly, not the color channel
                randomPixelPointsToExtractFrom = random.sample(
                    [[x, y] for x in range(len(frame)) for y in range(len(frame[0]))],
                    math.ceil(maxInformationHiddenPerFrame / 3))
                # Start Hiding in the frames
                for point in randomPixelPointsToExtractFrom:
                    # Move through the Colors in each pixel
                    for color in range(len(frame[point[0]][point[1]])):
                        # When all the bits are hidden break
                        if totalBitsRead > hiddenMessageInfromationSize:

                            if numberOfBitsExtracted == hiddenFileBitSize:
                                print("Finished Extracting")
                                break
                            extractedBit = frame[point[0]][point[1]][color] & 1
                            hiddenFileExtractedBits += str(extractedBit)
                            numberOfBitsExtracted += 1

                        totalBitsRead += 1
                    else:
                        continue
                    break  # If break then break out of entire loop
                else:
                    continue
                break  # same here

        self.progress = 70
        # Convert Bit Stream to Byte Stream and Get the Hash of the bit stream

        HiddenMessageInformationBinaryList = []
        BinaryString = ""

        i = 0
        for bit in hiddenFileExtractedBits:

            BinaryString += bit
            i += 1

            if i > 7:
                HiddenMessageInformationBinaryList.append(BinaryString)
                BinaryString = ""
                i = 0

        self.progress = 90

        generatedFileSignature = sha256(hiddenFileExtractedBits.encode('utf-8')).hexdigest()

        del hiddenFileExtractedBits

        HiddenMessageInformationAscii = []

        for BinaryString in HiddenMessageInformationBinaryList:
            HiddenMessageInformationAscii.append(int(BinaryString, 2))
        # HiddenMessageInformation = ""
        if hiddenFileSignature == generatedFileSignature:
            print("File Extracted Correctly")
        else:
            self.invalidSignatureError = True
            print("Failed")
        del HiddenMessageInformationBinaryList
        # for letter in HiddenMessageInformationAscii:
        #  HiddenMessageInformation += chr(letter)

        # Compare Generated Hash to Extracted Hash to test Integrity

        HiddenMessageInformationUnencrypted = AESCipher().decrypt(bytes(HiddenMessageInformationAscii), key, iv)

        self.progress = 95
        # Write Extracted File
        # if not os.path.exists("./Extracted Files"):
        # os.makedirs("Extracted Files")
        with open(extractPath + hiddenFileName, 'wb') as f:
            f.write(HiddenMessageInformationUnencrypted)

        self.progress = 100

        del HiddenMessageInformationAscii

        # del(HiddenMessageInformation)

        stegoVideo.release()
