import rsa
import requests

import base64

from ParseFiles import ParseXML


def getPublicKey(email):
    # https://www.geeksforgeeks.org/get-post-requests-using-python/

    # Important note
    # If errors occur with ssl: https://stackoverflow.com/questions/51390968/python-ssl-certificate-verify-error
    # and be sure to install it to the interpreter

    URL = "https://improved-uniquely-cheetah.ngrok-free.app/api/Users/GetPublicKey/" + email

    r = requests.get(url=URL)

    data = r.text

    # if I want the user can do
    # data = r.json()
    # publicKeyAsXML = data['publicKey']

    exponentString, modulusString = ParseXML.parsePublicKeyString(data)

    E = base64.b64decode(exponentString)
    public_E_int = int.from_bytes(E, byteorder='big', signed=False)

    M = base64.b64decode(modulusString)
    public_M_int = int.from_bytes(M, byteorder='big', signed=False)

    publicKeyDictionary = {'e': public_E_int, 'n': public_M_int}

    publicKey = rsa.PublicKey(n=publicKeyDictionary['n'], e=publicKeyDictionary['e'])

    return publicKey
