import json
import logging
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import boto3

@define
class AwsS3(BaseTool):
    # these aren't needed for boto3. it's checking ENV vars
    # remove if this is clear for users
    aws_access_key_id: str = field(default=None, kw_only=True, metadata={"env": "AWS_ACCESS_KEY_ID"})
    aws_secret_access_key: str = field(default=None, kw_only=True, metadata={"env": "AWS_SECRET_ACCESS_KEY"})

    @activity(config={
        "name": "list_buckets",
        "description": "can be used to list all s3 buckets in an aws account",
        "schema":  Schema({
            Literal(
                "aws_region",
                description="the aws region in which to create the boto3 session"
            ): str
        })
    })
    def list_buckets(self, value: bytes) -> BaseArtifact:
        try:
            s3 = boto3.client('s3')
            response = s3.list_buckets()
            return TextArtifact(response)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving s3 buckets {e}")

    @activity(config={
        "name": "upload_file",
        "description": "can be used to upload a file to an s3 bucket",
        "schema": Schema({
            Literal(
                "bucket_name",
                description="the name of the s3 bucket to upload the file to"
            ): str,
            Literal(
                "object_name",
                description="the name of the object to be created in the s3 bucket"
            ): str,
            Literal(
                "file_name",
                description="the name of the file to be uploaded"
            ): str
        })
    })
    def upload_file(self, value: bytes) -> BaseArtifact:
        try:
            s3 = boto3.client('s3')
            response = s3.upload_file(value.get("file_name"), value.get("bucket_name"), value.get("object_name"))
            return TextArtifact(response)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error uploading file to s3 bucket {e}")
