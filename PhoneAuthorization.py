# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC8331d7e8faeb9fc39c15c1f98ca19cff"
auth_token = "cb94219dbaef35274a719c570b1d1088"
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='Testing12345',
         from_='+15046366799',
         to='+970597033634'
     )

print(message.sid)