import os.path
from email import errors

import httplib2
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/userinfo.email']

currentEmail = ""
"""Shows basic usage of the Gmail API.
Lists the user's Gmail labels.
"""
creds = None
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

def authenticateUser():

    global creds, currentEmail


    if os.path.exists("../Gmail/token.json"):
        creds = Credentials.from_authorized_user_file("../Gmail/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "../Gmail/credentials.json", SCOPES  # https://stackoverflow.com/a/73071344/17870878
            )

            creds = flow.run_local_server(port=0)
            print(flow.authorization_url())

        # Save the credentials for the next run
        # with open("../Gmail/token.json", "w") as token:
        #     token.write(creds.to_json())

    URL = "https://www.googleapis.com/oauth2/v2/userinfo?access_token=" + creds.token

    response = requests.get(url=URL)

    currentEmail = response.json()['email']

    # Test to see if the API is working

    # try:
    #     # Call the Gmail API
    #     service = build("gmail", "v1", credentials=creds)
    #     results = service.users().labels().list(userId="me").execute()
    #     labels = results.get("labels", [])
    #
    #     if not labels:
    #         print("No labels found.")
    #     print("Labels:")
    #     for label in labels:
    #         print(label["name"])
    #
    # except HttpError as error:
    #     # TODO(developer) - Handle errors from gmail API.
    #     print(f"An error occurred: {error}")
