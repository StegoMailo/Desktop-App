
# Get an image
# Encrypt the image
# Use LSB algo
# Send the image via gmail

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)

# Create a MIMEMultipart message
message = MIMEMultipart()
message['to'] = '1202444@student.birzeit.edu'
message['subject'] = 'This is test'
message.attach(MIMEText('This is the body of the email'))

# Attach the image
with open('./watermarked.png', 'rb') as img_file:
    img_data = img_file.read()
    img_attachment = MIMEImage(img_data, name='watermarked.png')
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