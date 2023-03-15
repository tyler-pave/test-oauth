from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path

scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'https://mail.google.com/']

creds = None
# this is just seeing if you have a token already and if not will go through the OAuth flow
if os.path.exists('gmail-token.json'):
    creds = Credentials.from_authorized_user_file('gmail-token.json', scopes)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request()) 
    else:
        # OAUTH_CREDS are from https://console.cloud.google.com/apis/credentials
        flow = InstalledAppFlow.from_client_secrets_file('OAUTH_CREDS_PATH', scopes=scopes)
        creds = flow.run_local_server()
        credentials = flow.credentials
    with open('gmail-token.json', 'w') as token:
        token.write(creds.to_json())

# print(f'token - {credentials.token}')
# print(f'refresh - {credentials.refresh_token}')

service = build('gmail', 'v1', credentials=creds)
res = service.users().messages().list(userId='me').execute()
print(res)

