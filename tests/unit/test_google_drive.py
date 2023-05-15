from griptape.labs.tools import GoogleDrive

class TestGoogleDrive:
    def test_list_files_non_json_creds(self):
        assert "error parsing service account creds" in GoogleDrive(
            service_account_creds=""
        ).list_files({}).value

    def test_list_files(self):
        assert "error searching Drive" in GoogleDrive(
            service_account_creds="{}"
        ).list_files({}).value
