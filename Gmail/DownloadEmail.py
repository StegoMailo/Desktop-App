import base64
import os

from googleapiclient.discovery import build

from Gmail import AuthenticateEmail

stegoMail = []
subjects = []
senders = []
messageID = []
bodies = []
attachmentNames = []

def getAllStegoMail():
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=AuthenticateEmail.creds)

        # request a list of all the messages
        result = service.users().messages().list(userId='me',
                                                 q="{-from:me subject:stego has:attachment} OR from:me to:me subject:stego has:attachment").execute()


        # We can also pass maxResults to get any number of emails. Like this:
        # result = service.users().messages().list(maxResults=200, userId='me').execute()
        messages = result.get('messages')
        #print(messages)
        # messages is a list of dictionaries where each dictionary contains a message id.
        global stegoMail, subjects, senders, messageID, bodies
        stegoMail = []
        subjects = []
        senders = []
        messageID = []
        bodies = []

        # iterate through all the messages
        for msg in messages:
            stegoMail.append(msg)
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            #print(txt)
            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                #print("test")
                #print(headers[-3]['value'])

                subject = headers[-3]['value']
                subjects.append(subject)

                sender = headers[-2]['value']
                senders.append(sender)

                messageID.append(msg['id'])

                #print("Subject: ", subject)
                #print("sender: ", sender)

                # Look for Subject and Sender Gmail in the headers
                # for d in headers:
                #    # print(d)
                #     if d['name'] == 'Subject':
                #         subject = d['value']
                #         subjects.append(subject)
                #         #print("Subject: ", subject)
                #     if d['name'] == 'From':
                #         sender = d['value']
                #         senders.append(sender.split('<')[1].split('>')[0])
                #         messageID.append(msg['id'])
                #         #print("sender: ", sender.split('<')[1].split('>')[0])

                # The Body of the message is in Encrypted format. So, we have to decode it.
                # Get the data and decode it with base 64 decoder.
                #print(payload.get('parts')[0])

                parts = payload['parts'][0]
                #print("test")
                #print(txt['payload']['parts'][0])
                #print(parts['body']['data'])
                data = parts['body']['data']
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)
                body = decoded_data.decode('utf-8')
                #print(body)
                bodies.append(body)

                fileName = txt['payload']['parts'][1]['filename']
                attachmentNames.append(fileName)

                #print(txt['payload']['parts'][1]['filename'])

                # Printing the subject, sender's email and message
                # print("Subject: ", subject)
                # print("From: ", sender)
                # print("Message: ", body)
               # print('\n')
            except:
               #print("ERROR WHILE READING EMAILS")
                pass

    except Exception as error:
        print(f'An error occurred: {error}')


def downloadAttachment(messageID):
    service = build('gmail', 'v1', credentials=AuthenticateEmail.creds)
    message = service.users().messages().get(userId='me', id=messageID).execute()

    for part in message['payload']['parts']:
        if part['filename']:
            if 'data' in part['body']:
                data = part['body']['data']
            else:
                att_id = part['body']['attachmentId']
                att = service.users().messages().attachments().get(userId='me', messageId=messageID,
                                                                   id=att_id).execute()
                data = att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            path = part['filename']

            if not os.path.exists("./tempFiles"):
                os.makedirs("tempFiles")

            with open("./tempFiles/"+path, 'wb') as f:
                f.write(file_data)


# getAllStegoMail()
# downloadAttachment()
# print(stegoMail)

