import json
import logging
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
from zoomus import ZoomClient

@define
class Zoom(BaseTool):
    zoom_api_key: str = field(default=None, kw_only=True, metadata={"env": "ZOOM_API_KEY"})
    zoom_api_secret: str = field(default=None, kw_only=True, metadata={"env": "ZOOM_API_SECRET"})

    @activity(config={
        "name": "list_users",
        "description": "Can be used to list all users in a zoom account",
        "schema": Schema(
            str,
            description="context of this activity"
        )
    })
    def list_users(self, value: bytes) -> BaseArtifact:
        zoom_api_key = self.env_value("ZOOM_API_KEY")
        zoom_api_secret = self.env_value("ZOOM_API_SECRET")
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
        "name": "list_upcoming_zoom_meetings",
        "description": "can be used to list upcoming zoom meetings",
        "schema": Schema({
            Literal(
                "user_id",
                description="the user id associated with the zoom account that owns the meeting"
            ): str
        })
    })
    def list_upcoming_zoom_meetings(self, value: bytes) -> BaseArtifact:
        zoom_api_key = self.env_value("ZOOM_API_KEY")
        zoom_api_secret = self.env_value("ZOOM_API_SECRET")
        try:
            client = ZoomClient(zoom_api_key, zoom_api_secret)
            meeting_list = json.loads(client.meeting.list(user_id=value.get("user_id")).content)
            if meeting_list.get("code") == 124:
                return ErrorArtifact(f"error retrieving upcoming meetings from Zoom {meeting_list.get('message')}")
            return TextArtifact(meeting_list)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving upcoming meetings from Zoom {e}")
