from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from schema import Schema, Literal
from griptape.utils.decorators import activity
from griptape.utils import minify_json, CommandRunner
from griptape.labs.tools import BaseAwsTool
from attr import define, field


@define
class AwsCliTool(BaseAwsTool):
    aws_cli_policy: str = field(
        default="""{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}""",
        kw_only=True,
    )

    @property
    def schema_template_args(self) -> dict:
        return {"policy": minify_json(self.aws_cli_policy)}

    @activity(
        config={
            "description": "Can be used to execute AWS CLI v2 commands limited by this policy: {{ _self.schema_template_args['policy'] }}",
            "schema": Schema(
                {
                    Literal(
                        "command", description="AWS CLI v2 command starting with 'aws'"
                    ): str
                }
            ),
        }
    )
    def execute(self, params: dict) -> BaseArtifact:
        command = params["values"]["command"]
        result = CommandRunner().run(f"AWS_PAGER='' {command} --output json")

        if isinstance(result, ErrorArtifact):
            return result
        else:
            value = result.value

            if value == "":
                final_result = "[]"
            else:
                try:
                    final_result = minify_json(value)
                except Exception:
                    final_result = value

            return TextArtifact(final_result)
