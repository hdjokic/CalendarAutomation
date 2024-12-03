import os
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1ndzqhxWEzciYuENn6DwitdF5ex_LJBdP4HdClSc2tNw"

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
        sheets = service.spreadsheets()
        result = sheets.values().get(spreadsheetId = SPREADSHEET_ID, range = "SubSheet 2024!A1:B1").execute()

        values = result.get("values", [])

        for row in values:
            print(row)
        #add an event to the calendar----------------------------------------
        # event = {
        #     "summary": "My python event",
        #     "location": "Online",
        #     "description": "details",
        #     "colorId": 6,
        #     "start":{
        #         "dateTime": "2024-12-02T09:00:00+02:00",
        #         "timeZone": "America/Chicago"
        #     },
        #     "end": {
        #         "dateTime": "2024-12-02T12:00:00+02:00",
        #         "timeZone": "America/Chicago"
        #     },
        #     "attendees":[
        #         {"email": "hristtina99@gmail.com"}
        #     ]
        #
        # }
        # event = service.events().insert(calendarId="primary", body = event).execute()
        # print(f"Event created {event.get('htmlLink')}")

    except HttpError as error:
        print("An error occured: ", error)

        # LIST 10 EVENTS --------------------------------------------------
        # now = dt.datetime.now().isoformat() + "Z"
        #
        # events_result = (
        #     service.events()
        #     .list(
        #         calendarId="primary",
        #         timeMin = now,
        #         maxResults=10,
        #         singleEvents=True,
        #         orderBy="startTime",
        #    )
        #     .execute()
        # )
        # events = events_result.get("items", [])
        #
        # if not events:
        #     print("No upcoming events found")
        #     return
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"])
        # LIST 10 EVENTS--------------------------------------------------------------

if __name__ == "__main__":
    main()

