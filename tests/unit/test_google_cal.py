from griptape.labs.tools import GoogleCal

class TestGoogleCal:
    def test_get_events_non_json_creds(self):
        value = {
            "calendar_id": "primary"
        }
        assert "error parsing service account creds" in GoogleCal(
            service_account_creds=""
        ).get_upcoming_events(value).value

    def test_get_events(self):
        value = {
            "calendar_id": "primary"
        }
        assert "error retrieving calendar events" in GoogleCal(
            service_account_creds="{}"
        ).get_upcoming_events(value).value
