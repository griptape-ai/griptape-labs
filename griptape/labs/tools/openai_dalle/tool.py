import json
import logging
import os
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
from attr import define, field
import openai

@define
class OpenAiDallE(BaseTool):
    openai_api_key: str = field(default=None, kw_only=True, metadata={"env": "OPENAI_API_KEY"})

    @activity(config={
        "name": "create_image",
        "description": "can be used to create an image from text",
        "schema": Schema({
            Literal(
                "prompt",
                description="the prompt to use for the image generation"
            ): str,
            Literal(
                "size",
                description="length and width of the image to create in pixels. use the format NxN where N is an integer between 1 and 512"
            ): str,
            Literal(
                "file_name",
                description="the name of the file to be uploaded"
            ): str
        })
    })
    def create_image(self, params: dict) -> BaseArtifact:
        values = params["values"]
        try:
            openai.api_key = self.env_value("OPENAI_API_KEY")
            response = openai.Image.create(
                prompt=values["prompt"],
                n=1,
                size=values["size"]
            )
            return TextArtifact(response)
        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"error creating image with openai {e}")
