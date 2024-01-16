from xml.dom.minidom import parseString

def parsePublicKeyString( publicKeyXML):
    parsedPublicKeyXML = parseString(publicKeyXML)
    return parsedPublicKeyXML.getElementsByTagName("Exponent")[0].firstChild.nodeValue,\
        parsedPublicKeyXML.getElementsByTagName("Modulus")[0].firstChild.nodeValue

def parsePrivateKeyString( privateKeyXML):
    parsedPrivateKeyXML = parseString(privateKeyXML)

    return parsedPrivateKeyXML.getElementsByTagName("Exponent")[0].firstChild.nodeValue,\
    parsedPrivateKeyXML.getElementsByTagName("Modulus")[0].firstChild.nodeValue,\
    parsedPrivateKeyXML.getElementsByTagName("D")[0].firstChild.nodeValue,\
    parsedPrivateKeyXML.getElementsByTagName("P")[0].firstChild.nodeValue,\
    parsedPrivateKeyXML.getElementsByTagName("Q")[0].firstChild.nodeValue




