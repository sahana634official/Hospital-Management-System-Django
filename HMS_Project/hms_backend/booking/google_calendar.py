import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_DIR = os.path.join(BASE_DIR, "tokens")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "credentials.json")


def get_token_path(role, user_id):
    return os.path.join(TOKEN_DIR, f"{role}_{user_id}_token.json")


def connect_calendar(role, user_id):
    os.makedirs(TOKEN_DIR, exist_ok=True)

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    token_path = get_token_path(role, user_id)
    with open(token_path, "w") as token:
        token.write(creds.to_json())

    return True


def create_event(role, user_id, summary, description, start_dt, end_dt):
    token_path = get_token_path(role, user_id)

    if not os.path.exists(token_path):
        return None  # not connected yet

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_dt, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_dt, "timeZone": "Asia/Kolkata"},
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("htmlLink")
