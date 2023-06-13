from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact, ListArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import requests


@define
class ProxycurlClient(BaseTool):
    GET_PROFILE_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"

    api_key: str = field(kw_only=True)
    get_profile_params: dict = field(factory=dict, kw_only=True)

    timeout = field(default=30, kw_only=True)

    @activity(
        config={
            "description": "Can be used to get LinkedIn profile information for people",
            "schema": Schema({
                Literal(
                    "profile_id",
                    description="LinkedIn profile ID (i.e., https://www.linkedin.com/in/<profile_id>)"
                ): str
            }),
        }
    )
    def get_profile(self, params: dict) -> BaseArtifact:
        profile_id = params["values"]["profile_id"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = self.get_profile_params

        params["url"] = f"https://www.linkedin.com/in/{profile_id}"

        response = requests.get(
            self.GET_PROFILE_ENDPOINT, params=params, headers=headers, timeout=self.timeout
        )

        if response.status_code == 200:
            return ListArtifact.from_list([
                TextArtifact(str({key: value}))
                for key, value in response.json().items()
            ])
        else:
            return ErrorArtifact(
                f"Proxycurl returned an error with status code "
                f"{response.status_code} and reason '{response.reason}'"
            )
