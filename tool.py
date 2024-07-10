"""Base tool spec class."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from dotenv import find_dotenv, load_dotenv
from llama_index.core.bridge.pydantic import BaseModel, FieldInfo, create_model
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.tools.tool_spec.base import \
    BaseToolSpec as LlamaBaseToolSpec
from llama_index.core.tools.types import ToolMetadata

load_dotenv(find_dotenv())
SPEC_FUNCTION_TYPE = Union[str, Tuple[str, str]]


class BaseToolSpec(LlamaBaseToolSpec):
    """Base tool spec class."""

    FIELD_DESCRIPTIONS = {}

    def __init__(self):
        """Initialize with parameters."""
        self.chutiya = "chutiya"

    def get_fn_schema_from_fn_name(
        self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
    ) -> Optional[Type[BaseModel]]:
        response = super().get_fn_schema_from_fn_name(fn_name, spec_functions)

        # print(f"getting schema for fn_name: {fn_name}")
        # print(f"response schema: {response.schema_json()}")

        if fn_name in self.FIELD_DESCRIPTIONS:
            required_fields = [
                name for name, field in response.__fields__.items() if field.required
            ]
            fields = {
                name: (field.outer_type_, field.default)
                for name, field in response.__fields__.items()
            }

            for field_name, description in self.FIELD_DESCRIPTIONS[fn_name].items():
                if field_name in fields:
                    current_type, current_default = fields[field_name]
                    fields[field_name] = self.field_with_description(
                        current_type, current_default, description
                    )

            response = create_model(fn_name, **fields)

            # Manually set the required fields in the schema after model creation
            schema = response.schema()
            schema["required"] = required_fields

            # If you need the schema to reflect these changes in all subsequent calls:
            response.schema = lambda *args, **kwargs: schema

        # print(f"response schema after: {response.schema_json()}")

        return response

    def field_with_description(self, type_, default_value, description):
        if default_value is ...:
            return (type_, FieldInfo(..., description=description))
        else:
            return (type_, FieldInfo(default_value, description=description))

    def get_metadata_from_fn_name(
        self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
    ) -> Optional[ToolMetadata]:
        """Return map from function name.

        Return type is Optional, meaning that the schema can be None.
        In this case, it's up to the downstream tool implementation to infer the schema.

        """
        try:
            func = getattr(self, fn_name)
        except AttributeError:
            return None
        name = fn_name
        docstring = func.__doc__ or ""
        description = f"{docstring}"
        fn_schema = self.get_fn_schema_from_fn_name(
            fn_name, spec_functions=spec_functions
        )
        return ToolMetadata(name=name, description=description, fn_schema=fn_schema)


class DoctorTool(BaseToolSpec):

    FIELD_DESCRIPTIONS = {
        "upload_image": {},
        "my_availability": {},
        "talk_to_human_agent": {},
        "skip_response_to_the_user": {},
        # "talk_to_human_agent": {"sql_query": "Sql query"}
    }

    spec_functions = [
        "upload_image",
        "my_availability",
        "talk_to_human_agent",
        "skip_response_to_the_user",
    ]

    def upload_image(self):
        """
Use this when user wants to upload a image
"""
        return "Here is the image upload popup. click on this button"
        # return "Here is the image upload popup, please upload the image"

    def my_availability(self):
        """
Use this when user wants to schedule their availability, working hours
"""
        return "Ask user to select date and time from this pop up"

    def talk_to_human_agent(self):
        """
Use this when user wants to talk to a human agent
"""
        return "Tell user we are connecting you to a human agent"

    def skip_response_to_the_user(self):
        """
Skip the response to the user

Use this function when you want to skip responding to the user.
This is useful when you don't want to sound repetetive or annoying.
This is also useful when the user sends a message that is not relevant to the conversation or when the user sends a message that is not actionable.
If you exectue this function no message will be sent to the user in response.
"""
        return "SUCCESS. No response will be sent to the user."

    def create_optimized_sql_query(
        self,
        optmized_sql_query: str,
        runtime_of_optimized_sql_query: float,
        runtime_of_given_sql_query: float,
    ):
        # if runtime_of_optimized_sql_query < runtime_of_given_sql_query:
        return (
            f"Show the user only the optimized sql query and runtime of optimised sql query like a "
            f"python list: {[optmized_sql_query, runtime_of_optimized_sql_query]} "
            f"Don't write anything else"
        )
