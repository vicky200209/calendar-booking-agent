from pydantic import BaseModel
class EventRequest(BaseModel):
    summary: str
    start: str
    end: str
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
import pickle

app = FastAPI()

# Optional: allow frontend to connect later (Streamlit or browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_calendar_service():
    creds = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=creds)
    return service

@app.get("/")
def home():
    return {"message": "Calendar Booking API is running."}

@app.get("/availability/")
def check_availability(start: str, end: str):
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return {
        "available": len(events) == 0,
        "events": events
    }

@app.post("/book/")
async def book_event(data: EventRequest):
    service = get_calendar_service()
    event = {
        'summary': data.summary,
        'start': {
            'dateTime': data.start,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': data.end,
            'timeZone': 'Asia/Kolkata',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return {
        "message": "Event created successfully!",
        "event_link": event.get('htmlLink')
    }
    

