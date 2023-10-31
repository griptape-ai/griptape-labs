import shotgun_api3
from schema import Schema, Literal, Optional
from attr import define, field, Factory
from griptape.artifacts import TextArtifact, ErrorArtifact, InfoArtifact, ListArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
import pprint

# sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)


@define
class ShotgridClient(BaseTool):
    """
    Attributes:
        site: The URL of your Shotgrid server
        script_name: Name of the API script registered in Shotgrid.
        script_key: API key of the script registered in Shotgrid.
    """

    site: str = field(default=str, kw_only=True)
    script_name: str = field(default=str, kw_only=True)
    script_key: str = field(default=str, kw_only=True)

    @activity(
        config={
            "description": "Retrieve all projects from Shotgrid.",
            "schema": Schema({}),
        }
    )
    def retrieve_all_projects(self, params: dict) -> ListArtifact | ErrorArtifact:
        list_artifact = ListArtifact()

        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            # Find all projects
            projects = sg.find("Project", [], ["id", "name"])

            return ListArtifact([TextArtifact(str(p)) for p in projects])

        except Exception as e:
            return ErrorArtifact(f"Error retrieving projects: {e}")

    @activity(
        config={
            "description": "Can be used to retrieve a list of entities from Shotgrid.",
            "schema": Schema(
                {
                    Literal(
                        "entity_type",
                        description="Entity Type. Examples: Project, Asset, Sequence, Shot",
                    ): str,
                    Literal(
                        "filters",
                        description="""Shotgrid filters. Example:
                        List all assets that have a status of "ip" in project id 70: [["project": {"type": "Project", "id": 70}],["sg_status_list", "is", "ip"],["assets", "is", {"type": "Asset", "id": 9}]]""",
                    ): list,
                },
            ),
        }
    )
    def retrieve_entities(self, params: dict) -> ListArtifact | ErrorArtifact:
        list_artifact = ListArtifact()

        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            fields = ["id", "code", "sg_asset_type", "sg_status_list"]
            # Find all assets for a project
            assets = sg.find(
                params["values"]["entity_type"], params["values"]["filters"], fields
            )

            print("----- Returned from Shotgrid -----")
            print(assets)
            print("----------------------------------")
            return ListArtifact([TextArtifact(str(a)) for a in assets])

        except Exception as e:
            return ErrorArtifact(f"Error retrieving assets: {e}")

    @activity(
        config={
            "description": "Can be used to retrieve information about an asset.",
            "schema": Schema(
                {Literal("code", description="The name of an Asset"): str}
            ),
        }
    )
    def retrieve_matching_assets(self, params: dict) -> ListArtifact | ErrorArtifact:
        list_artifact = ListArtifact()
        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            filters = [["code", "is", params["values"]["code"]]]

            fields = [
                "code",
                "description",
                "sg_asset_type",
                "project",
                "created_at",
                "updated_at",
                "sg_status_list",
            ]

            # Find all matching assets
            assets = sg.find("Asset", filters, fields)

            return ListArtifact([TextArtifact(str(a)) for a in assets])

        except Exception as e:
            return ErrorArtifact(f"Error retrieving asset information: {e}")

    @activity(
        config={
            "description": "Can be used to create an entity.",
            "schema": Schema(
                {
                    Literal(
                        "entity_type", description="Shotgun entity type to create."
                    ): str,
                    Literal("entity_name", description="The name of the asset"): str,
                    Literal(
                        "data",
                        description="Dictionary of fields and corresponding values to set on the new entity. \
                    If image or filmstrip_image fields are provided, the file path will be uploaded \
                    to the server automatically.",
                    ): dict,
                    Literal(
                        "return_fields",
                        description="Optional list of additional field values to return from the new entity. Defaults to id field.",
                    ): list,
                }
            ),
        }
    )
    def create_an_entity(self, params: dict) -> ListArtifact | ErrorArtifact:
        list_artifact = ListArtifact()

        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            params["values"]["data"]["code"] = params["values"]["entity_name"]

            # Create the shot
            result = sg.create(
                params["values"]["entity_type"],
                params["values"]["data"],
                params["values"]["return_fields"],
            )

            return ListArtifact([TextArtifact(str(a)) for a in result])

        except Exception as e:
            return ErrorArtifact(f"Error creating the entity: {e}")

    @activity(
        config={
            "description": "Can be used to update an entity.",
            "schema": Schema(
                {
                    Literal("entity_type", description="Entity type to update."): str,
                    Literal(
                        "entity_id",
                        description="id of the entity to update.",
                    ): int,
                    Literal(
                        "data",
                        description="key/value pairs where key is the field name and value is the value to\
                    set for that field. This method does not restrict the updating of fields hidden \
                    in the web UI via the Project Tracking Settings panel. ",
                    ): dict,
                    Optional(
                        "multi_entity_update_modes",
                        description="Optional dict indicating what update mode to use when updating a multi-entity link field. \
                    The keys in the dict are the fields to set the mode for, \
                    and the values from the dict are one of set, add, or remove. Defaults to set.",
                    ): dict,
                }
            ),
        }
    )
    def update_an_entity(self, params: dict) -> ListArtifact | ErrorArtifact:
        list_artifact = ListArtifact()

        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            # params["values"]["data"]["code"] = params["values"]["entity_name"]

            # Update the entity
            result = sg.update(
                params["values"]["entity_type"],
                params["values"]["entity_id"],
                params["values"]["data"],
            )

            return ListArtifact([TextArtifact(str(a)) for a in result])

        except Exception as e:
            return ErrorArtifact(f"Error updating the entity: {e}")

    @activity(
        config={
            "description": "Can be used to delete/retire an entity.",
            "schema": Schema(
                {
                    Literal("entity_type", description="Entity type to delete."): str,
                    Literal(
                        "entity_id", description="id of the entity to delete."
                    ): int,
                }
            ),
        }
    )
    def delete_an_entity(self, params: dict) -> InfoArtifact | ErrorArtifact:
        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            # delete the entity
            result = sg.delete(
                params["values"]["entity_type"], params["values"]["entity_id"]
            )

            return InfoArtifact(True)

        except Exception as e:
            return ErrorArtifact(f"Error deleting the entity: {e}")

    @activity(
        config={
            "description": "Can be used to revive an entity.",
            "schema": Schema(
                {
                    Literal("entity_type", description="Entity type to revive."): str,
                    Literal("entity_id", description="id of the entity to reive."): int,
                }
            ),
        }
    )
    def revive_an_entity(self, params: dict) -> InfoArtifact | ErrorArtifact:
        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            # revive the entity
            result = sg.revive(
                params["values"]["entity_type"], params["values"]["entity_id"]
            )

            return InfoArtifact(True)

        except Exception as e:
            return ErrorArtifact(f"Error reviving the entity: {e}")

    @activity(
        config={
            "description": "Can be used to upload a thumbnail to a shotgrid entity. Supported image types are .jpg, .png, .gif, .tif, .tiff, .bmp, .exr, .dpx, .tga",
            "schema": Schema(
                {
                    Literal(
                        "entity_type",
                        description="Entity type to set the thumbnail for.",
                    ): str,
                    Literal(
                        "entity_id",
                        description="Id of the entity to set the thumbnail for.",
                    ): int,
                    Literal(
                        "path", description="Full path to the thumbnail file on disk."
                    ): str,
                }
            ),
        }
    )
    def upload_thumbnail(self, params: dict) -> TextArtifact | ErrorArtifact:
        try:
            # Connect to shotgrid
            sg = shotgun_api3.Shotgun(
                self.site, script_name=self.script_name, api_key=self.script_key
            )

            # delete the entity
            result = sg.upload_thumbnail(
                params["values"]["entity_type"],
                params["values"]["entity_id"],
                params["values"]["path"],
            )

            return TextArtifact(result)

        except Exception as e:
            return ErrorArtifact(f"Error reviving the entity: {e}")
