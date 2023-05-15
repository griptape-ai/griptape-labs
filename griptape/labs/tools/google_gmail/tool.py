import json
import logging
import base64
from email.message import EmailMessage
from schema import Schema, Literal
from attr import define, field
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from google.oauth2 import service_account
from googleapiclient.discovery import build

@define
class GoogleGmail(BaseTool):
    service_account_creds: str = field(default=None, kw_only=True, metadata={"env": "GOOGLE_SERVICE_ACCOUNT_CREDS"})

    @activity(config={
        "name": "create_draft_email",
        "description": "Can be used to create a draft email in gmail",
        "schema": Schema({
            Literal(
                "to",
                description="email address to send to"
            ): str,
            Literal(
                "subject",
                description="subject of the email"
            ): str,
            Literal(
                "from",
                description="email address to send from"
            ): str,
            Literal(
                "body",
                description="body of the email"
            ): str,
            Literal(
                "inbox_owner",
                description="email address of the inbox owner where the draft will be created. if not provided, use the from address"
            ): str
        })
    })
    def create_draft_email(self, params: dict) -> BaseArtifact:
        values = params["values"]
        # Scopes are purposely defined within activity to allow for more granular control
        scopes = ['https://www.googleapis.com/auth/gmail.compose']
        try:
            service_account_creds = json.loads(self.env_value("GOOGLE_SERVICE_ACCOUNT_CREDS"))
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error parsing service account creds {e}")

        try:
            creds = service_account.Credentials.from_service_account_info(service_account_creds, scopes=scopes)
            delegated_creds = creds.with_subject(values["inbox_owner"])
            service = build('gmail', 'v1', credentials=delegated_creds)

            message = EmailMessage()
            message.set_content(values["body"])
            message['To'] = values["to"]
            message['From'] = values["from"]
            message['Subject'] = values["subject"]

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                'message': {
                    'raw': encoded_message
                }
            }
            draft = service.users().drafts().create(userId='me', body=create_message).execute()
            return TextArtifact(f'Draft Id: {draft["id"]}')
        except Exception as error:
            logging.error(error)
            return ErrorArtifact(f'Error creating draft email: {error}')
