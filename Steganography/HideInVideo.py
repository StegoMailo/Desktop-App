import math
import os
import random
import re
from hashlib import sha256

import cv2
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip

from Cipher.AES import AESCipher


class HideInVideo():

    def IntegerToBinaryString(self, number):
        return '{0:08b}'.format(number)

    def hideInVideo(self, coverVideoPath, fileToHidePath, useAudio, seed=-1,key=-1):
        # Open Cover Video

        coverVideo = cv2.VideoCapture(coverVideoPath)

        # Get Frame Information

        width = int(coverVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(coverVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        colorChannels = 3

        maxInformationHiddenPerFrame = int((height * width * colorChannels))  # In bits
        # Get total number of bits than use 1/8th
        # Can multiply 8 and divide by 8

        # Get the number of frames in the video

        length = int(coverVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = math.ceil(coverVideo.get(cv2.CAP_PROP_FPS))

        # Maximum Possible Message That Can be hidden

        maxMessageSize = (height * width * colorChannels * length)  # In bits

        # Get total number of bits then divide by 8
        # Can multiply 8 and divide by 8

        # Load File to Hide

        fileName = os.path.basename(fileToHidePath)

        with open(fileToHidePath, 'rb') as fp:
            hiddenFileByteStream = fp.read()

        ##Prepare File

        # Encrypt File

        hiddenFileByteStream, key, iv = AESCipher().encrypt(hiddenFileByteStream,key)

        # Convert Byte Stream to ASCII Integers From Hex

        hiddenFileAsBinaryString = ""

        for byte in hiddenFileByteStream:
            hiddenFileAsBinaryString += f'{byte:08b}'

        # Store Important File Information To Hide Later

        # Get Hash of the Hidden File Byte Stream

        fileHash = sha256(hiddenFileAsBinaryString.encode('utf-8')).hexdigest()

        hiddenFileBitStreamSize = len(hiddenFileAsBinaryString)
        hiddenFileInformationToHide = str(hiddenFileBitStreamSize) + "|" + fileHash + "|" + fileName + "|"

        # Convert It to ASCII Integers

        informationAsASCII = []

        for letter in hiddenFileInformationToHide:
            informationAsASCII.extend(ord(num) for num in letter)

        # Convert ASCII Integers to Binary

        hiddenFileInformationBitStream = []

        for num in informationAsASCII:
            hiddenFileInformationBitStream.append(self.IntegerToBinaryString(num))

        # Make the Binary list into one long String

        hiddenFileInformationBitStreamString = "".join(hiddenFileInformationBitStream)

        # Combine important information to hide

        informationToHide = hiddenFileInformationBitStreamString + "|" + hiddenFileAsBinaryString

        # Get Size of Everything that will be hidden

        sizeOfInformationToBeHidden = len(informationToHide)

        # Check to See if the Information Will Fit

        if sizeOfInformationToBeHidden > maxMessageSize - 10:  # Calculations are done in bits
            print("File too big to hide!")

        # Number of Frames That will be used

        numberOfFramesToBeUsed = int(math.ceil(sizeOfInformationToBeHidden / maxInformationHiddenPerFrame))

        # Hide the information in the Frames

        # Can use the user's system instead of ram to store information.
        if not os.path.exists("./tempFiles"):
            os.makedirs("tempFiles")
            if not os.path.exists("./tempFiles/tempFrames"):
                os.makedirs("./tempFiles/tempFrames")
        temp_folder = "./tempFiles/tempFrames"

        if seed == -1:
            seed = random.randint(0,
                                  9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
        seedToShare = seed
        random.seed(seed)
        # Generate Random Frame Access
        randomFrameAccess = random.sample(range(numberOfFramesToBeUsed), numberOfFramesToBeUsed)
        # randomFrameAccess = list(range(numberOfFramesToBeUsed))
        # accessedFrames = []
        numberOfBitsHidden = 0
        coverVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Iterate Video through the random frames
        for frameNumber in randomFrameAccess:
            # Select the random frame
            coverVideo.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
            res, frame = coverVideo.read()
            # Check to see if the frame is readable
            if not res:
                print("Video Contains Bad Frame")
                break
            else:
                # change the seed and generate random pixel points in the frame to hide bits in
                seed += 361
                random.seed(seed)
                # (math.ceil()/3) is done because the pixel is chosen randomly, not the color channel
                randomPixelPointsToHideIn = random.sample(
                    [[x, y] for x in range(len(frame)) for y in range(len(frame[0]))],
                    math.ceil(maxInformationHiddenPerFrame / 3))
                # Start Hiding in the frames
                for point in randomPixelPointsToHideIn:
                    # Move through the Colors in each pixel
                    for color in range(len(frame[point[0]][point[1]])):
                        # When all the bits are hidden break
                        if numberOfBitsHidden == sizeOfInformationToBeHidden:
                            # accessedFrames.append(frame)
                            cv2.imwrite(os.path.join(temp_folder, "tempFrame_" + str(frameNumber) + ".png"), frame)
                            print("Finished Hiding")
                            break
                        # Change LSB to 1 if needed
                        if informationToHide[numberOfBitsHidden] == '1':
                            frame[point[0]][point[1]][color] |= 1
                        else:
                            # Change LSB to 0 if needed
                            frame[point[0]][point[1]][color] &= ~1

                        numberOfBitsHidden += 1
                    else:
                        continue
                    break  # If break then break out of entire loop
                else:
                    # accessedFrames.append(frame)
                    cv2.imwrite(os.path.join(temp_folder, "tempFrame_" + str(frameNumber) + ".png"), frame)
                    continue
                break  # same here

        self.__saveVideoFrames(fps, width, height)
        if (useAudio):
            self.__addAudioToVideo(coverVideoPath, './tempFiles/tempFinalVideoWithoutSound.avi')

        coverVideo.release()

        return seedToShare, key, iv

    # Save GIF

    # TODO
    def __saveVideoFrames(self, fps, width, height):
        # Save Only Stego Frames
        fourcc = cv2.VideoWriter.fourcc(*'ffv1')  # ffv1
        finalVideo = cv2.VideoWriter('./tempFiles/tempFinalVideoWithoutSound.avi', fourcc, fps, (width, height))
        frameProgress = 0
        tempFramesDirectory = "./tempFiles/tempFrames"
        frames = sorted(os.listdir(tempFramesDirectory), key=lambda s: int(re.findall(r'\d+', s)[0]))
        for frame in frames:
            # finalVideo.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
            finalVideo.write(cv2.imread(tempFramesDirectory + "/" + frame))
            frameProgress += 1
            # print("Frame Progress: " + str(frameProgress))

        finalVideo.release()
        # del (accessedFrames)

    # *Optional*
    def __addAudioToVideo(self, orginalVideo, stegoVideo):
        # Save Audio to Stego Frames

        # Extract audio
        video = VideoFileClip(orginalVideo)
        video.audio.write_audiofile("./tempFiles/tempAudio.wav")
        # I don't know what default does exactly, pcm_s32le is lossless. (pc encoding)
        # There is also pcm_s16le

        # Cut and Save Audio
        video_clip = VideoFileClip(stegoVideo)
        audio_clip = AudioFileClip("./tempFiles/tempAudio.wav").set_duration(video_clip.duration)
        audio_clip.write_audiofile("./tempFiles/tempAudioCut.wav")

        video = ffmpeg.input(stegoVideo)
        audio = ffmpeg.input('./tempFiles/tempAudioCut.wav')
        videoPath = "./tempFiles/finalVideoWithAudio.avi"
        out = ffmpeg.output(video, audio, videoPath, vcodec='copy', acodec='copy', strict='experimental')

        # can use , acodec='flac' but this will prevent
        # traversing the video, VLC crashes
        # acodec='copy' lossless I think, Allows for traversing the video
        # Default acodec may be lossly
        # can use aac for lossy audio but very small space
        try:
            out.run(capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e
