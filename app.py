from flask import Flask, request, send_file
import os
import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from ics import Calendar, Event, Attendee

app = Flask(__name__)

# Google Sheets credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/calendar"]
SPREADSHEET_ID = "1ndzqhxWEzciYuENn6DwitdF5ex_LJBdP4HdClSc2tNw"

# Load credentials from file
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# Create a service object for the Google Sheets API
service = build("sheets", "v4", credentials=creds)

# Create a service object for the Google Calendar API
calendar_service = build("calendar", "v3", credentials=creds)

# Define a function to add an event to the calendar
def add_event_to_calendar(event_data):
    try:
        event = calendar_service.events().insert(calendarId="primary", body=event_data).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define a function to add an event to the ICS file
def add_event_to_ics_file(event):
    c = Calendar()
    e = Event()
    e.name = event["summary"]
    e.begin = event["start"]["dateTime"]
    e.end = event["end"]["dateTime"]
    e.description = event["class category"]
    e.attendees = [Attendee(event["attendees"]["email"])]
    c.events.add(e)
    return c

# Define a route to generate the ICS file
@app.route("/generate-ics", methods=["POST"])
def generate_ics():
    sheet_link = request.json["sheetLink"]
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet45!A2:ZZ").execute()
    values = result.get("values", [])
    events = []
    for row in values:
        start_time, end_time = row[5].split("-")
        start_time = dt.datetime.strptime(start_time.strip(), "%H")
        end_time = dt.datetime.strptime(end_time.strip(), "%H")
        start_time = start_time.replace(year=dt.date.today().year, month=dt.date.today().month, day=dt.date.today().day)
        end_time = end_time.replace(year=dt.date.today().year, month=dt.date.today().month, day=dt.date.today().day)
        if row[6] == "Hristina P":
            event_data = {
                "summary": "LSF2 tennis",
                "class category": row[1],
                "start": {"dateTime": start_time.isoformat(), "timeZone": "America/Chicago"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "America/Chicago"},
                "attendees": {"email": "hristtina99@gmail.com"},
            }
            events.append(event_data)
    ics_file = Calendar()
    for event in events:
        ics_file = add_event_to_ics_file(event)
    return send_file(ics_file.to_ics(), as_attachment=True, attachment_filename="events.ics")

if __name__ == "__main__":
    app.run(debug=True)