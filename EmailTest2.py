
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
from Steganography.ExtractFromImage import ExtractFromImage
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Set the path to your credentials JSON file
credentials_path = 'credentials.json'

# Define the required Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials


def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def parse_parts(service, parts, folder_name, message):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            filepath = ""
            key, iv = None, None
            seed = 0
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType.startswith('image') or mimeType.startswith('video'):
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            # we get the attachment ID
                            # and make another request to get the attachment itself
                            filepath = os.path.join('./attachments/', filename)
                            print("Saving the file:", filepath, "size:", get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages() \
                                .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")

                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))

                            print(seed)
                            print(key)
                            print(iv)

                            ExtractFromImage().extractFromImage(filepath, './Extracted Files/', int(seed), key, iv)

            elif mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
                    seed, key, iv = text.split('|')[1:4]

                    ExtractFromImage().extractFromImage(filepath, './Extracted Files/', int(seed), key, iv)

            # else:
            #     # attachment other than a plain text or HTML
            #     for part_header in part_headers:
            #         part_header_name = part_header.get("name")
            #         part_header_value = part_header.get("value")
            #         if part_header_name == "Content-Disposition":
            #             if "attachment" in part_header_value:
            #                 # we get the attachment ID
            #                 # and make another request to get the attachment itself
            #                 filepath = os.path.join('../attachments/', filename)
            #                 print("Saving the file:", filepath, "size:", get_size_format(file_size))
            #                 attachment_id = body.get("attachmentId")
            #                 attachment = service.users().messages() \
            #                             .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
            #                 data = attachment.get("data")
            #
            #                 if data:
            #                     with open(filepath, "wb") as f:
            #                         f.write(urlsafe_b64decode(data))


def read_message(service, message):
    """
    This function takes Gmail API service and the given message_id and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "./attachments"
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # make a directory with the name of the subject
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)

    parse_parts(service, parts, folder_name, message)
    print("=" * 50)


credentials = None
token_path = 'token.json'

# The file token.json stores the user's access and refresh tokens
# if os.path.exists(token_path):
#     credentials = Credentials.from_authorized_user_file(token_path)

# If there are no (valid) credentials available, let the user log in

if not credentials or not credentials.valid:
    credentials = authenticate()

    # Save the credentials for the next run
    with open(token_path, 'w') as token:
        token.write(credentials.to_json())

# Build the Gmail API service
service = build('gmail', 'v1', credentials=credentials)

results = search_messages(service, "Stego|")
print(f"Found {len(results)} results.")
# for each email matched, read it (output plain/text to console & save HTML and attachments)
for msg in results:
    read_message(service, msg)