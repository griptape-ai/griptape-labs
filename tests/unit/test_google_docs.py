from griptape.labs.tools import GoogleDocs


class TestGoogleDocs:
    def test_get_title_non_json_creds(self):
        value = {
            "document_id": "invalid_id"
        }
        assert "error parsing service account creds" in GoogleDocs(
            service_account_creds=""
        ).get_title({"values": value}).value

    def test_get_title(self):
        value = {
            "document_id": "invalid_id"
        }
        assert "error retrieving document" in GoogleDocs(
            service_account_creds="{}"
        ).get_title({"values": value}).value
