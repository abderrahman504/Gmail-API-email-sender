from __future__ import print_function

import base64
from email.message import EmailMessage
import os.path
# import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

import time
import csv


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())



def gmail_send_message(reciever: str):

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content("""التسجيل لمسابقة Let\'s Make a Robot سينتهى يوم الخميس\n
                            التسجيل يبدأ من الساعة 10 صباحا الى الساعة 3 مساء فى شارع انتاج فى كلية هندسة\n
                            
                            """)

        message['To'] = reciever
        message['From'] = 'dev.abdelrahmankh@gmail.com'
        message['Subject'] = 'Let\'s Make a Robot registration has started!'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message



if __name__ == '__main__':
    mailsSentCounter = 0
    breakCounter = 0
    with open('LET\'S MAKE A ROBOT COMPETITION 2023 (Responses) - Form responses 1.csv', newline='', encoding='utf-8') as f:
        first: bool = True
        reader = csv.reader(f)
        for row in reader:
            if first: 
                first = False
                continue
            reciever = row[3]
            gmail_send_message(reciever)
            mailsSentCounter += 1
            breakCounter += 1
            if breakCounter > 50:
                breakCounter = 0
                time.sleep(0.1)
    fh = open("number of mails sent.txt", "w")
    fh.write(str(mailsSentCounter))
    fh.close()


