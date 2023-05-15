import json
import logging
import datetime
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from google.oauth2 import service_account
from googleapiclient.discovery import build
from schema import Schema, Literal
from attr import define, field

@define
class GoogleCal(BaseTool):
    service_account_creds: str = field(default=None, kw_only=True, metadata={"env": "GOOGLE_SERVICE_ACCOUNT_CREDS"})
    @activity(config={
        "name": "get_upcoming_events",
        "description": "Can be used to get upcoming events from a google calendar",
        "schema": Schema({
            Literal(
                "calendar_id",
                description="id of the google calendar such as 'primary'"
            ): str
        })
    })
    def get_upcoming_events(self, params: dict) -> BaseArtifact:
        values = params["values"]
        scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        try:
            service_account_creds = json.loads(self.env_value("GOOGLE_SERVICE_ACCOUNT_CREDS"))
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error parsing service account creds {e}")

        calendar_id = values["calendar_id"]

        try:
            creds = service_account.Credentials.from_service_account_info(service_account_creds, scopes=scopes)
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + 'Z'

            events_result = service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=10, singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving calendar events {e}")

        if not events:
            return ErrorArtifact("No upcoming events found.")
        else:
            return TextArtifact(events)