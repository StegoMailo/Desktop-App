import base64
import mimetypes
import os
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Gmail import AuthenticateEmail


def gmail_send_message(to:str,subject:str,attachmentPath:str,messageToSend:str,attachmentName:str):
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

    mime_message["To"] = to
    #mime_message["To"] = "guineapigsarecute3748@gmail.com"
    mime_message["From"] = AuthenticateEmail.currentEmail
    mime_message["Subject"] = subject

    # attachment
    #attachment_filename = os.path.basename(attachmentPath)
    # guessing the MIME type
    type_subtype, _ = mimetypes.guess_type(attachmentName)
    maintype, subtype = type_subtype.split("/")

    with open(attachmentPath, "rb") as fp:
      attachment_data = fp.read()
    mime_message.add_attachment(attachment_data, maintype, subtype,filename=attachmentName)

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

#gmail_send_message("Testing123")