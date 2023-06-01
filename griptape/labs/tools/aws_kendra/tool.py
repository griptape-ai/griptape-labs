import json
import logging
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import boto3

@define
class AwsKendraClient(BaseTool):
    index_id: str = field(default=None, kw_only=True)

    @activity(config={
        "name": "query",
        "description": "Can be used to query an AWS Kendra index.",
        "schema": Schema({
            Literal(
                "queryText",
                description="The query text passed to the AWS Kendra index.",
            ): str,
        })
    })
    def query(self, params: dict) -> BaseArtifact:
        try:
            kendra = boto3.client('kendra')
            query_text = params['values']["queryText"]
            response = kendra.query(IndexId=self.index_id, QueryText=query_text)
            response_text = ''
            for query_result in response["ResultItems"]:
                if query_result["Type"]=="ANSWER" or query_result["Type"]=="QUESTION_ANSWER":
                    answer_text = query_result["DocumentExcerpt"]["Text"]
                    response_text += answer_text + "\n"

                if query_result["Type"]=="DOCUMENT":
                    if "DocumentTitle" in query_result:
                        document_title = query_result["DocumentTitle"]["Text"]
                        response_text += document_title + "\n"
                    document_text = query_result["DocumentExcerpt"]["Text"]
                    response_text += document_text + "\n"

            return TextArtifact(response_text)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"Error querying Kendra: {e}")
