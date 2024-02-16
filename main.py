import os
from Keys import GetPublicKey
from Steganography.ExtractFromImage import ExtractFromImage
from Steganography.HideInImage import HideInImage
from Steganography.ExtractFromVideo import ExtractFromVideo
from Steganography.HideInVideo import HideInVideo
import time

start = time.time()
#seed, key, iv = HideInVideo().hideInVideo("Goku Super Saiyan.mp4", "Goku Super Saiyan.mp4", True)

#print("Finished Hiding")
#ExtractFromVideo().extractFromVideo('./tempFiles/finalVideoWithAudio.avi', seed, key, iv)

# email = "guineapigsarecute3748@gmail.com"

# publicKey = GetPublicKey.getPublicKey(email)
# print(publicKey)
# privateKey = LoadPrivateKey.loadPrivateKey()
#
# message = 'I Love Shawarma'.encode(('utf-8'))
# cipherText = rsa.encrypt(message, publicKey)
#
# extractedMessage = rsa.decrypt(cipherText, privateKey)
#
# print("Message: "+str(message)[2:][:-1])
#
# print("Cipher Text: "+str(cipherText))
#
# print("Extracted Message: "+str(extractedMessage)[2:][:-1])
# Slicing was done just to remove the b''


# Going to use something like this to store private key
# URL = "https://localhost:7121/api/Users/GetAll"
# r = requests.get(url=URL, verify=False)
#
# data = r.json()
# print(data[0]['privateKey'])

seed, key,iv = HideInImage().hideInImage('cat.jpg','largetext.txt',"watermarked2.png")
print("Finished Hiding")
if not os.path.exists("./Extracted Files"):
    os.makedirs("Extracted Files")

ExtractFromImage().extractFromImage("watermarked2.png","./Extracted Files/",seed, key, iv)

print("Finished")
end = time.time()
print((end - start))
