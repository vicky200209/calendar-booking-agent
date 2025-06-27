from googleapiclient.discovery import build
import pickle

# Load credentials
creds = pickle.load(open("token.pkl", "rb"))

# Build calendar service
service = build("calendar", "v3", credentials=creds)

# Fetch upcoming 5 events
events_result = service.events().list(
    calendarId='primary',
    maxResults=5,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

if not events:
    print("No upcoming events found.")
else:
    print("Upcoming events:")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"- {start}: {event['summary']}")
