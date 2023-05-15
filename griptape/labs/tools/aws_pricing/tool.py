import json
import logging
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import boto3

@define
class AwsPricing(BaseTool):
    aws_access_key_id: str = field(default=None, kw_only=True, metadata={"env": "AWS_ACCESS_KEY_ID"})
    aws_secret_access_key: str = field(default=None, kw_only=True, metadata={"env": "AWS_SECRET_ACCESS_KEY"})
    @activity(config={
        "name": "get_pricing",
        "description": "can be used to get pricing information about aws services",
        "schema": Schema({
            Literal(
                "service_code",
                description="the aws product service code, such as AmazonEC2, to be used in the get_products call"
            ): str,
            Literal(
                "filter_type",
                description="the type parameter to use in the get_products filter such as 'TERM_MATCH'"
            ): str,
            Literal(
                "product_family",
                description="the value to use for the productFamily field such as 'Fast Snapshot Restore'"
            ): str,
            Literal(
                "aws_region",
                description="the aws region in which to create the boto3 session"
            ): str
        })
    })
    def get_pricing(self, params: dict) -> BaseArtifact:
        values = params["values"]
        try:
            session = boto3.session.Session(region_name=values["aws_region"])
            client = session.client("pricing")
            prices = client.get_products(
                ServiceCode=values["service_code"],
                Filters=[
                    {
                        'Type': values["filter_type"],
                        'Field': 'productFamily',
                        'Value': values["product_family"]
                    }
                ]
            )
            return TextArtifact(json.dumps(prices))
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving aws pricing info {e}")
