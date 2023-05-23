from typing import Optional, Union
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact, ListArtifact
from schema import Schema, Literal
from griptape.core import BaseTool
from griptape.core.decorators import activity
from attr import define, field
from stability_sdk import api
from stability_sdk.animation import AnimationArgs, Animator

@define
class StableAnim(BaseTool):
    STABILITY_HOST = 'grpc.stability.ai:433'
    stability_key: str = field(default=None, kw_only=True, metadata={"env": "stability_key"})
    @activity(config={
        "description": "Can be used to create animations from text",
        "pass_artifacts": True
    })
    def animate(self, params: dict) -> Union[ErrorArtifact, ListArtifact]:
            return ListArtifact([])
