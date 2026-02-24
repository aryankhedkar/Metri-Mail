import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    """
    Returns an authenticated Gmail API service object.
    On first run, opens a browser for OAuth consent.
    After that, uses the saved token.
    """
    creds = None

    if os.path.exists(Config.GMAIL_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(Config.GMAIL_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.GMAIL_CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(Config.GMAIL_TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
