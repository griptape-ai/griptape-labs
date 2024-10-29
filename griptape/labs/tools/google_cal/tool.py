import logging
import datetime
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.utils.decorators import activity
from attr import define

from griptape.labs.tools.base_google_tool import BaseGoogleTool


@define
class GoogleCalTool(BaseGoogleTool):
    READ_CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    @activity(
        config={
            "description": "Can be used to get upcoming events from a google calendar",
        }
    )
    def get_upcoming_events(self, params: dict) -> BaseArtifact:
        try:
            service = self._build_client(
                scopes=self.READ_CALENDAR_SCOPES,
                service_name="calendar",
                version="v3",
            )
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving calendar events {e}")

        if not events:
            return ErrorArtifact("No upcoming events found.")
        else:
            return TextArtifact(events)
