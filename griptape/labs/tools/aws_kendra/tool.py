import json
import logging
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact, ListArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import boto3


@define
class AwsKendraClient(BaseTool):
    index_id: str = field(kw_only=True)

    @activity(
        config={
            "name": "query",
            "description": "Can be used to query an AWS Kendra index.",
            "schema": Schema(
                {
                    Literal(
                        "query_text",
                        description="The query text passed to the AWS Kendra index.",
                    ): str,
                }
            ),
        }
    )
    def query(self, params: dict) -> BaseArtifact:
        try:
            kendra = boto3.client("kendra")
            query_text = params["values"]["query_text"]

            response = kendra.query(IndexId=self.index_id, QueryText=query_text)
            list_artifact = ListArtifact()
            for query_result in response["ResultItems"]:
                if (
                    query_result["Type"] == "ANSWER"
                    or query_result["Type"] == "QUESTION_ANSWER"
                ):
                    answer_text = TextArtifact(query_result["DocumentExcerpt"]["Text"])
                    list_artifact.value.append(answer_text)
                elif query_result["Type"] == "DOCUMENT":
                    if "DocumentTitle" in query_result:
                        document_title = query_result["DocumentTitle"]["Text"]
                    document_text = query_result["DocumentExcerpt"]["Text"]
                    list_artifact.value.append(
                        TextArtifact(f"Title: {document_title}\n{document_text}")
                    )

            return list_artifact
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"Error querying Kendra: {e}")
