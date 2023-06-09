from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import requests


@define
class ProxycurlClient(BaseTool):
    api_key: str = field(default=None, kw_only=True)

    api_endpoint: str = field(default="https://nubela.co/proxycurl/api/v2/linkedin", kw_only=True)

    @activity(
        config={
            "name": "get_profile",
            "description": "Can be used to get a user's LinkedIn profile information.",
            "schema": Schema(
                {Literal("profile_id", description="Profile id of LinkedIn user."): str}
            ),
        }
    )
    def get_profile(self, params: dict) -> BaseArtifact:
        profile_id = params["values"]["profile_id"]
        header_dic = {"Authorization": "Bearer " + self.api_key}
        params = {
            "url": f"https://www.linkedin.com/in/{profile_id}",
        }

        response = requests.get(
            self.api_endpoint, params=params, headers=header_dic, timeout=30
        )
        print(response.json())

        if response.status_code == 200:
            return TextArtifact(response.json())
        return ErrorArtifact(
            f"Proxycurl returned an error with status code "
            f"{response.status_code} and reason '{response.reason}'"
        )