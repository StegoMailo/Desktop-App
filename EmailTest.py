# Get an image
# Encrypt the image
# Use LSB algo
# Send the image via gmail

import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from Steganography.HideInImage import HideInImage



def filePath(fileName):
    return os.path.join(folder_name,fileName)
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)
folder_name='TestFiles/'
mediaName = "./TestFiles/cat.jpg"
secreteFile = "./TestFiles/largetext.txt"
outputFileName = "watermarked.png"

key, seed, iv = HideInImage().hideInImage((mediaName), (secreteFile), (f'./{folder_name}'+outputFileName))

# Create a MIMEMultipart message
sendTo = "tahajamal891@gmail.com"
subject = 'this is a test message'
body = 'Stego|'+str(key)+'|'+str(seed)+'|'+str(iv)+'| \n hello there'

message = MIMEMultipart()
message['to'] = sendTo
message['subject'] = subject
message.attach(MIMEText(body))


# Attach the image
with open('./TestFiles/'+outputFileName, 'rb') as img_file:
    img_data = img_file.read()
    img_attachment = MIMEImage(img_data, name=outputFileName)
    message.attach(img_attachment)

# Encode the message as base64
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

create_message = {'raw': raw_message}

try:
    sent_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f'Sent message to {sent_message} Message Id: {sent_message["id"]}')
except HTTPError as error:
    print(f'An error occurred: {error}')
    sent_message = None