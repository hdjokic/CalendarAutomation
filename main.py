import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import (Credentials)

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www/googleapis.com/auth/calendar"]

def main():

    #how to authenticate
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())


