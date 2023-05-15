from griptape.artifacts import BaseArtifact
from griptape.labs.tools import AwsPricing

class TestAwsPrice:

    def test_get_price(self):
        value = {
            "service_code": "AmazonEC2",
            "filter_type": "TERM_MATCH",
            "product_family": "Compute Instance",
            "aws_region": "us-east-1"
        }
        assert isinstance(AwsPricing().get_pricing({"values":value}), BaseArtifact)
        # assert "error retrieving aws pricing info" in AwsPricing(
        #     aws_secret_access_key="",
        #     aws_access_key_id=""
        # ).get_pricing(value).value

