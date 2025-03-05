from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_people_with_access(service, file_id):
    """
    Retrieves a list of people with access to a Google Sheet.

    Args:
        service (googleapiclient.discovery.Resource): The Google Drive API service.
        file_id (str): The ID of the Google Sheet.

    Returns:
        list: A list of dictionaries containing information about the people with access.
    """
    permissions = service.permissions().list(fileId=file_id, fields='permissions(emailAddress,role)').execute()
    people_with_access = []
    for permission in permissions.get('permissions', []):
        people_with_access.append({
            'email': permission.get('emailAddress'),
            'role': permission.get('role')
        })
    return people_with_access

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    file_id = '1ndzqhxWEzciYuENn6DwitdF5ex_LJBdP4HdClSc2tNw'
    people_with_access = get_people_with_access(service, file_id)
    print(people_with_access)

if __name__ == '__main__':
    main()