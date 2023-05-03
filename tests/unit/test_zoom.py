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
