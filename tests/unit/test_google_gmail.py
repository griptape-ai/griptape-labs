from griptape.labs.tools import GoogleGmail

class TestGoogleGmail:
    def test_create_draft_email_non_json_creds(self):
        value = {
            "to": "hello@griptape.ai",
            "subject": "hello",
            "body": "this is a test email.",
            "from": "tony@griptape.ai"
        }
        assert "error parsing service account creds" in GoogleGmail(
            service_account_creds=""
        ).create_draft_email(value).value

    def test_get_events(self):
        value = {
            "to": "hello@griptape.ai",
            "subject": "hello",
            "body": "this is a test email.",
            "from": "tony@griptape.ai"
        }
        assert "Error creating draft email" in GoogleGmail(
            service_account_creds="{}"
        ).create_draft_email(value).value
