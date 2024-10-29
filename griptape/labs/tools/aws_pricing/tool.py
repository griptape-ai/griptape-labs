import json
import logging
from typing import TYPE_CHECKING
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.labs.tools import BaseAwsTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define, field
from griptape.utils.decorators import lazy_property


if TYPE_CHECKING:
    from mypy_boto3_pricing import PricingClient


@define
class AwsPricing(BaseAwsTool):
    _client: PricingClient = field(
        default=None, kw_only=True, alias="client", metadata={"serializable": False}
    )

    @lazy_property()
    def client(self) -> PricingClient:
        return self.session.client("pricing")

    @activity(
        config={
            "description": "can be used to get pricing information about aws services",
            "schema": Schema(
                {
                    Literal(
                        "service_code",
                        description="the aws product service code, such as AmazonEC2, to be used in the get_products call",
                    ): str,
                    Literal(
                        "filter_type",
                        description="the type parameter to use in the get_products filter such as 'TERM_MATCH'",
                    ): str,
                    Literal(
                        "product_family",
                        description="the value to use for the productFamily field such as 'Fast Snapshot Restore'",
                    ): str,
                    Literal(
                        "aws_region",
                        description="the aws region in which to create the boto3 session",
                    ): str,
                }
            ),
        }
    )
    def get_pricing(self, params: dict) -> BaseArtifact:
        values = params["values"]
        try:
            client = self.session.client("pricing")
            prices = client.get_products(
                ServiceCode=values["service_code"],
                Filters=[
                    {
                        "Type": values["filter_type"],
                        "Field": "productFamily",
                        "Value": values["product_family"],
                    }
                ],
            )
            return TextArtifact(json.dumps(prices))
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error retrieving aws pricing info {e}")
