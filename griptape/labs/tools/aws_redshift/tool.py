import logging
import time
from typing import Optional
from attr import define, field
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.core import BaseTool
from griptape.core.decorators import activity
from schema import Schema, Literal
import boto3


@define
class AwsRedshiftClient(BaseTool):
    database: str = field(default=None, kw_only=True)

    workgroup_name: str = field(default=None, kw_only=True)

    aws_region_name = field(default=None, kw_only=True)

    @activity(
        config={
            "name": "execute_statement",
            "description": "Can be used to execute AWS Redshift statements.",
            "schema": Schema(
                {
                    Literal(
                        "sql", description="AWS Redshift SQL statement to execute."
                    ): str
                }
            ),
        }
    )
    def execute_statement(self, params: dict) -> BaseArtifact:
        try:
            sql = params["values"]["sql"]

            redshift_data = boto3.client(
                "redshift-data", region_name=self.aws_region_name
            )
            response = redshift_data.execute_statement(
                Sql=sql,
                Database=self.database,
                WorkgroupName="default",
            )

            statement = redshift_data.describe_statement(Id=response["Id"])
            while statement["Status"] == "PICKED":
                time.sleep(1)
                statement = redshift_data.describe_statement(Id=response["Id"])
            if statement["Status"] == "FINISHED":
                statement_result = redshift_data.get_statement_result(Id=response["Id"])
                data = statement_result.get("Records", [])
                while "NextToken" in statement_result:
                    statement_result = redshift_data.get_statement_result(
                        Id=response[id], NextToken=statement_result["NextToken"]
                    )
                    data = data + response.get("Records", [])
                return TextArtifact(data)
            if statement["Status"] == "FAILED":
                return ErrorArtifact(f"Error querying redshift: {statement['Error']}")

        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"Error executing statement: {e}")

    @activity(
        config={
            "name": "list_tables",
            "description": "Can be used to list AWS Redshift tables.",
            "schema": Schema({}),
        }
    )
    def list_tables(self, params: dict) -> BaseArtifact:
        try:
            redshift_data = boto3.client(
                "redshift-data", region_name=self.aws_region_name
            )
            response = redshift_data.list_tables(
                Database=self.database,
                WorkgroupName=self.workgroup_name,
            )

            table_names = [table["name"] for table in response["Tables"]]
            while "NextToken" in response:
                response = redshift_data.list_tables(
                    Id=response[id],
                    NextToken=response["NextToken"],
                )
                table_names = [
                    table["name"] for table in response["Tables"]
                ]
                tables = table_names + table_names
            return TextArtifact(table_names)

        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"Error listing tables: {e}")

    @activity(
        config={
            "name": "list_schemas",
            "description": "Can be used to list AWS Redshift schemas.",
            "schema": Schema({}),
        }
    )
    def list_schemas(self, params: dict) -> BaseArtifact:
        try:
            redshift_data = boto3.client(
                "redshift-data", region_name=self.aws_region_name
            )
            response = redshift_data.list_schemas(
                Database=self.database,
                WorkgroupName=self.workgroup_name,
            )

            schema_names = list(response['Schemas'])
            while "NextToken" in response:
                response = redshift_data.list_schemas(
                    Id=response[id],
                    NextToken=response["NextToken"],
                )
                schema_names = list(response['Schemas'])
                schema_names = schema_names + schema_names
            return TextArtifact(schema_names)

        except Exception as e:
            logging.error(e)
            return ErrorArtifact(f"Error listing schemas: {e}")
