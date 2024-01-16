from ParseFiles import ParseXML
import base64
import rsa


def loadPrivateKey():
    with open('myPrivateKey.txt') as f:
        privateKeyXMLString = f.read().replace("\n", "").replace("\r", "")
    exponentString, modulusString, dString, pString, qString = ParseXML.parsePrivateKeyString(privateKeyXMLString)

    E = base64.b64decode(exponentString)
    private_E_int = int.from_bytes(E, byteorder='big', signed=False)

    M = base64.b64decode(modulusString)
    private_M_int = int.from_bytes(M, byteorder='big', signed=False)

    P = base64.b64decode(pString)
    private_P_int = int.from_bytes(P, byteorder='big', signed=False)

    Q = base64.b64decode(qString)
    private_Q_int = int.from_bytes(Q, byteorder='big', signed=False)

    D = base64.b64decode(dString)
    private_D_int = int.from_bytes(D, byteorder='big', signed=False)

    old_priv_key = {'e': private_E_int, 'n': private_M_int, 'd': private_D_int, 'p': private_P_int, 'q': private_Q_int}

    priv_key = rsa.PrivateKey(n=old_priv_key['n'], e=old_priv_key['e'],
                              d=old_priv_key['d'], p=old_priv_key['p'], q=old_priv_key['q'])

    return priv_key
