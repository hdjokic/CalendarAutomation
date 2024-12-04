import os
import datetime as dt
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/calendar"]
SPREADSHEET_ID = "1ndzqhxWEzciYuENn6DwitdF5ex_LJBdP4HdClSc2tNw"


#add event to calendar
def add_event_to_calendar(service, event_data):
    try:
        event = service.events().insert(calendarId="primary", body=event_data).execute()
        print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")
def main():
    #how to authenticate
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    #if no creds available let user sign in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        #save creds to token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        #get calendar service
        service = build("sheets", "v4", credentials = creds)
        calendarService = build("calendar", "v3", credentials=creds)
        sheets = service.spreadsheets()

        result = sheets.values().get(spreadsheetId = SPREADSHEET_ID, range = "Sheet45!A2:ZZ").execute()

        values = result.get("values", [])

        for row in values:
            start_time, end_time = row[5].split('-')
            print(start_time)
            print(end_time)
            start_time = dt.datetime.strptime(start_time.strip(), "%H")
            end_time = dt.datetime.strptime(end_time.strip(), "%H")

            start_time = start_time.replace(year=dt.date.today().year, month=dt.date.today().month,day=dt.date.today().day)
            end_time = end_time.replace(year=dt.date.today().year, month=dt.date.today().month, day=dt.date.today().day)
            if row[6] == "Hristina P":
                event_data = {
                    'summary': 'LSF tennis',
                    'class category': row[1],
                    'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/Chicago'},
                    'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/Chicago'},
                    'attendees': [{'email':"hristtina99@gmail.com"}]
                }
                print(event_data)
                add_event_to_calendar(calendarService, event_data)

    except HttpError as error:
        print("An error occured: ", error)

if __name__ == "__main__":
    main()

