import mimetypes

import AuthenticateEmail


import base64
from email.message import EmailMessage

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_send_message(messageToSend:str):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = AuthenticateEmail.creds

  try:
    service = build("gmail", "v1", credentials=creds)
    mime_message = EmailMessage()

    mime_message.set_content(messageToSend)

    mime_message["To"] = "1202444@student.birzeit.edu"
    #mime_message["To"] = "guineapigsarecute3748@gmail.com"
    mime_message["From"] = "guineapigsarecute3748@gmail.com"
    mime_message["Subject"] = "Stego Testing"

    # attachment
    attachment_filename = "Goku Super Saiyan.mp4"
    # guessing the MIME type
    type_subtype, _ = mimetypes.guess_type(attachment_filename)
    maintype, subtype = type_subtype.split("/")

    with open(attachment_filename, "rb") as fp:
      attachment_data = fp.read()
    mime_message.add_attachment(attachment_data, maintype, subtype,filename=attachment_filename)

    # encoded message
    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

gmail_send_message("Testing123")