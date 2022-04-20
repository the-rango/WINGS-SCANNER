from PIL import Image
import glob
import time

# Save all png images as a single pdf
images = [Image.open(filename) for filename in glob.glob('*.png')]
images[0].save("wings.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
print('pdf created')

# Upload pdf to Google Drive
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os.path


SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/drive']


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
        print(creds)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

drive_service = build('drive', 'v3', credentials=creds)

file_metadata = {
    'name': 'wings.pdf',
    'mimeType': 'application/vnd.google-apps.document'
}
media = MediaFileUpload('wings.pdf',
                        mimetype='application/vnd.google-apps.document',
                        resumable=True)
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
fid = file.get('id')
print('File ID: %s' % fid)

# time.sleep(10)
