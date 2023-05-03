from griptape.labs.tools import Zoom

class TestZoom:
    def test_list_users(self):
        assert "error retrieving user list from Zoom" in Zoom(
            zoom_api_key="",
            zoom_api_secret=""
        ).list_users("").value

    def list_upcoming_zoom_meetings(self):
        assert "error retrieving upcoming meetings from Zoom" in Zoom(
            zoom_api_key="",
            zoom_api_secret="",
        ).list_upcoming_zoom_meetings({"user_id": ""}).value

    def test_create_zoom_meeting(self):
        assert "error creating zoom meeting" in Zoom(
            zoom_api_key="",
            zoom_api_secret="",
        ).create_zoom_meeting({"user_id": "", "topic": "", "start_time": ""}).value