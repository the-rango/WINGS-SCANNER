from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/drive']

# The ID of a sample document.
DOCUMENT_ID = '1KeAcV3m0vdWeaW9PxQ5M42j1lyVg-TmkTe-2pLSpPfo'

def read_doc(doc):
    '''Recursively look for textual content'''
    pltext = ''
    for k, v in doc.items():
        if type(v) is list:
            for ele in v:
                if type(ele) is dict:
                    pltext += read_doc(ele)
        elif type(v) is dict:
            pltext += read_doc(v)
        elif k == 'content' and isinstance(v, str):
            pltext += v
    return pltext


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
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
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        body = document.get('body')

        # pprint.pprint(body)
        pprint.pprint(read_doc(body))



    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
