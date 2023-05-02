from griptape.artifacts import BaseArtifact, TextArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from schema import Schema
from attr import define, field

@define
class GoogleDrive(BaseTool):
    service_account_file: str = field(default=None, kw_only=True, metadata={"env": "GOOGLE_SERVICE_ACCOUNT_FILE"})

    @activity(config={
        "name": "list_files",
        "description": "Can be used to list all files in a google drive",
        "schema": Schema(
            str,
            description="path to list all files"
        )
    })
    def list_files(self, value: bytes) -> BaseArtifact:
        scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        service_account_file = self.env_value("GOOGLE_SERVICE_ACCOUNT_FILE")
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes)

        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return TextArtifact("No files found.")
        else:
            return TextArtifact(items)