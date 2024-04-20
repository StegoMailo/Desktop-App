from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from base64 import b64encode
from base64 import b64decode


# https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode
class AESCipher():
    def encrypt(self, data, key=-1):
        if key == -1 or len(key) != 32:
            key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_CBC)
        cipherTextBytes = cipher.encrypt(pad(data, AES.block_size))
        # It's best to convert the iv, key and plain text to base 64 to reduce space
        ivB64 = b64encode(cipher.iv).decode('utf-8')
        keyB64 = b64encode(key).decode('utf-8')
        return cipherTextBytes, keyB64, ivB64

    def decrypt(self, cipherText, key, ivB64):
        iv = b64decode(ivB64)
        key = b64decode(key)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plainText = unpad(cipher.decrypt(cipherText), AES.block_size)
        return plainText

# # Example usage
# data = bytes('secretData', 'utf-8')
#
# # Encryption
# aes_cipher = AESCipher()
# cipherText, key, iv = aes_cipher.encrypt(data)
# print("Cipher Text:", str(cipherText) + " Key: " + str(key) + " IV: " +str(iv))
# # Decryption
# decrypted_data = aes_cipher.decrypt(cipherText, key, iv)
# print("Decrypted:",  decrypted_data.decode('utf-8'))
