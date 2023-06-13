import json
import logging
import datetime
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
from zoomus import ZoomClient


@define
class Zoom(BaseTool):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    zoom_api_key: str = field(kw_only=True)
    zoom_api_secret: str = field(kw_only=True)

    @activity(config={
        "description": "Can be used to list all users in a zoom account",
        "schema": Schema(
            str,
            description="context of this activity"
        )
    })
    def list_users(self, param: dict) -> BaseArtifact:
        zoom_api_key = self.zoom_api_key
        zoom_api_secret = self.zoom_api_secret

        try:
            client = ZoomClient(zoom_api_key, zoom_api_secret)
            users_response = client.user.list()
            user_list = json.loads(users_response.content)
            if user_list.get("code") == 124:
                return ErrorArtifact(f"error retrieving user list from Zoom {user_list.get('message')}")
            return TextArtifact(user_list)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving user list from Zoom {e}")

    @activity(config={
        "description": "can be used to list upcoming zoom meetings",
        "schema": Schema({
            Literal(
                "user_id",
                description="the user id associated with the zoom account that owns the meeting"
            ): str
        })
    })
    def list_upcoming_zoom_meetings(self, params: dict) -> BaseArtifact:
        values = params["values"]
        zoom_api_key = self.zoom_api_key
        zoom_api_secret = self.zoom_api_secret

        try:
            client = ZoomClient(zoom_api_key, zoom_api_secret)
            meeting_list = json.loads(client.meeting.list(user_id=values["user_id"]).content)
            if meeting_list.get("code") == 124:
                return ErrorArtifact(f"error retrieving upcoming meetings from Zoom {meeting_list.get('message')}")
            return TextArtifact(meeting_list)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving upcoming meetings from Zoom {e}")

    @activity(config={
        "description": "can be used to create a zoom meeting. first, use the list_users activity to get a list of users",
        "schema": Schema({
            Literal(
                "user_id",
                description="the id of the user that owns the zoom account"
            ): str,
            Literal(
                "topic",
                description="the topic of the meeting"
            ): str,
            Literal(
                "start_time",
                description=f"the start time of the meeting in {DATE_FORMAT} format"
            ): str,
            Literal(
                "duration",
                description="the duration of the meeting in minutes"
            ): int
        })
    })
    def create_zoom_meeting(self, params: dict) -> BaseArtifact:
        values = params["values"]
        zoom_api_key = self.zoom_api_key
        zoom_api_secret = self.zoom_api_secret

        try:
            client = ZoomClient(zoom_api_key, zoom_api_secret)
            response = client.meeting.create(
                topic=values["topic"],
                start_time=datetime.datetime.strptime(values["start_time"], self.DATE_FORMAT),
                duration=values["duration"],
                user_id=values["user_id"]
            )
            return TextArtifact(response)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error creating zoom meeting {e}")