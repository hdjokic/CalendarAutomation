import os
import datetime as dt
import datetime
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from ics import Calendar, Event, Attendee
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import mailer

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/calendar"]
SPREADSHEET_ID = "1ndzqhxWEzciYuENn6DwitdF5ex_LJBdP4HdClSc2tNw"

c = Calendar()
#add event to calendar
def add_event_to_calendar(service, event_data):
    try:
        event = service.events().insert(calendarId="primary", body=event_data).execute()
        print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")

#add event to ics file
def add_event_ics_file(event):
    first_attendee = Attendee(event['attendees']['email'])
    all_attendees = {first_attendee}


    e = Event()

    e.name = event['summary']
    e.begin = event['start']['dateTime']
    e.end = event['end']['dateTime']
    e.description = event['class category']
    e.attendees = all_attendees
    print(type(e.attendees))
    print(event['dtstamp'])
    #e.extra = dt.date('Ymd', event['dtstamp'])
    e.created = event['dtstamp']
    print (e.created)

    print('#####################')
    #print(e.extra)

    ##Below only needed if attendees_with_email Attendee object is not in dictionary
    #e.attendees = {attendees_with_email}


    #print('events attendees_with_email: ' + str(e.attendees))
    create_url(e)
    c.events.add(e)

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
        now = dt.datetime.now()

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
                    'summary': 'LSF2 tennis',
                    'class category': row[1],
                    'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/Chicago'},
                    'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/Chicago'},
                    'attendees': {'email' : 'hristtina99@gmail.com'},
                    'dtstamp': now

                }
                print(event_data)
                add_event_ics_file(event_data)
                #add_event_to_calendar(calendarService, event_data)

        with open("events.ics", "w") as f:
            print(c.serialize())
            f.write(c.serialize())

            #DEPRECATED - don't use str(c) or c in a serializable context
            #f.write(str(c))
            #ENDDEPRECATED
            # Remove empty lines from the ICS file
        with open("events.ics", "r") as f:
            lines = [line for line in f.read().splitlines() if line.strip()]

        with open("events.ics", "w") as f:
            for line in lines:
                f.write(line + '\n')

    except HttpError as error:
        print("An error occured: ", error)


def create_url(e):
    start = dt.datetime.now()
    end = dt.datetime.now()

    formatted_start = start.strftime("%Y%m%dT%H%M%S")
    formatted_end = end.strftime("%Y%m%dT%H%M%S")

    print("form start:"+formatted_start)

    timestamp = str(formatted_start) + '%2F' + str(formatted_end)
    print(timestamp)

    detail_text = 'HiThisIsDetails'
    text_text = 'HiThisIs%20Text'

    href_start = ("https://calendar.google.com/calendar/render?action=TEMPLATE")
    dates ="&dates="+ timestamp
    details = "&details=" + detail_text
    text="&text=" + text_text
    full_url = href_start+dates+details+text
    print(full_url)
    mailer.send_email('hristtina99@gmail.com', "this is the url to add to cal: "+ full_url)


    #20220112T180000Z%2F20220112T200000Z&details=Learn%20all%20about%20the%20rules%20of%20the%20Motorway%20and%20how%20to%20access%20the%20fast%20lane.%0A%0Ahttps%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGridlock_%28Doctor_Who%29&location=New%20Earth&text=Welcome%20to%20the%20Motorway")




if __name__ == "__main__":
    main()

