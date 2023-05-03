import json
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from schema import Schema, Literal
from attr import define, field

@define
class GoogleDocs(BaseTool):
    service_account_creds: str = field(default=None, kw_only=True, metadata={"env": "GOOGLE_SERVICE_ACCOUNT_CREDS"})
    @activity(config={
        "name": "get_title",
        "description": "Can be used to get title of a google doc",
        "schema": Schema({
            Literal(
                "document_id",
                description="id of the google document"
            ): str
        })
    })
    def get_title(self, value: bytes) -> BaseArtifact:
        scopes = ['https://www.googleapis.com/auth/documents.readonly']
        service_account_creds = json.loads(self.env_value("GOOGLE_SERVICE_ACCOUNT_CREDS"))
        document_id = value.get("document_id")

        try:
            creds = service_account.Credentials.from_service_account_info(service_account_creds, scopes=scopes)
            service = build('docs', 'v1', credentials=creds)
            document = service.documents().get(documentId=document_id).execute()
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving document {e}")

        if not document:
            return ErrorArtifact("No document found.")
        else:
            return TextArtifact(document.get('title'))