from typing import Union
from attr import define, field
from griptape.artifacts import ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity


@define
class StableAnim(BaseTool):
    STABILITY_HOST = 'grpc.stability.ai:433'
    stability_key: str = field(default=None, kw_only=True, metadata={"env": "stability_key"})

    @activity(config={
        "description": "Can be used to create animations from text",
    })
    def animate(self, params: dict) -> Union[ErrorArtifact, list]:
        return []
