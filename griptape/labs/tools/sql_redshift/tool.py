from typing import Optional
from attr import define, field
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal

@define
class SqlRedshiftClient(BaseTool):
    @activity(config={
        "name": "query",
        "description": "Can be used to execute SQL queries{% if engine %} in {{ engine }}{% endif %}",
        "schema": Schema({
            Literal(
                "query",
                description="SQL query to execute. For example, SELECT, CREATE, INSERT, DROP, DELETE, etc."
            ): str
        })
    })
    def query(self, params: dict) -> BaseArtifact:
       return BaseArtifact("not yet implemented")
