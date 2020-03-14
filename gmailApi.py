from __future__ import print_function
import pickle
import os.path
import base64
from tika import parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    user_id="me"
    query="from:jorge88888888@hotmail.com is:unread ticket "
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages=[]
    fileExtension=""
    i=0
    if "messages" in response:
        messages.extend(response["messages"])
        for obj in messages:
            messageId=obj["id"]
            message = service.users().messages().get(userId=user_id, id=messageId).execute()
            for part in message['payload']['parts']:
                extension = os.path.splitext(part['filename'])
                if extension == ".pdf":
                    attachmentId=part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(userId=user_id, id=attachmentId, messageId=messageId).execute()
                    file_data = base64.urlsafe_b64decode(attachment["data"].encode('UTF-8'))
                    path = "asd"+str(i)+".pdf"
                    f = open(path, 'wb')
                    f.write(file_data)
                    f.close()
                    i+=1
                    raw = parser.from_file("asd.pdf")
                    text = raw["content"].strip()
                    text = text.split("\n")
                    spaceFlag = True
                    for string in text:
                        if string and spaceFlag:
                            if string[0].isdigit():
                                stringArr=string.split(" ")
                                qnty=stringArr[0]
                                unitPrice = stringArr[len(stringArr)-3]
                                subtotal = stringArr[len(stringArr)-2]
                                item = " ".join(stringArr[1:len(stringArr)-3])
                                print(qnty)#to db
                                print(unitPrice)
                                print(subtotal)
                                print(item)
                            elif string[0]=="*":
                                stringArr=string.split(" ")
                                total = stringArr[len(stringArr)-1]
                                print(total)#to db
                                spaceFlag =  False
                            elif string[0].isalpha:
                                category = string
                                print(category)

if __name__ == '__main__':
    main()