import json
import logging
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
    service_account_creds: str = field(kw_only=True)

    @activity(config={
        "description": "Can be used to get title of a google doc",
        "schema": Schema({
            Literal(
                "document_id",
                description="id of the google document"
            ): str
        })
    })
    def get_title(self, params: dict) -> BaseArtifact:
        values = params["values"]
        scopes = ['https://www.googleapis.com/auth/documents.readonly']
        try:
            service_account_creds = json.loads(self.service_account_creds)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error parsing service account creds {e}")

        document_id = values["document_id"]

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