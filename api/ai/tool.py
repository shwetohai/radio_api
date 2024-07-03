from typing import Any, Dict, List, Optional, Type
from dotenv import find_dotenv, load_dotenv
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from pydantic import BaseModel, Field, create_model
import ast

class AllTool(BaseToolSpec):
    """
    SQLQueryOptimizerTool: Provides functionalities to optimize SQL queries and measure their performance
    """

    def __init__(self, FIELD_DESCRIPTIONS, spec_functions: List[str]) -> None:
        self.FIELD_DESCRIPTIONS = FIELD_DESCRIPTIONS
        self.spec_functions = spec_functions
        # self.runtime_sql_query = runtime_sql_query

    def upload_image(self):

        #call that api which will popup the choose file option
        # post()

        return "Here is the image upload popup. click on this button" 
        #return "Here is the image upload popup, please upload the image"
    
    def my_availability(self):

        #we can write anything here
        #call any other api to popup the box

        return "Ask user to select date and time from this pop up"
    
    def talk_to_human_agent(self):
        return "Tell user we are connecting you to a human agent"
    
    def skip_response_to_the_user(self):
        return "SUCCESS. No response will be sent to the user."

    def create_optimized_sql_query(
        self,
        optmized_sql_query: str,
        runtime_of_optimized_sql_query: float,
        runtime_of_given_sql_query: float,
    ):
        # if runtime_of_optimized_sql_query < runtime_of_given_sql_query:
        return f"Show the user only the optimized sql query and runtime of optimised sql query like a "\
                f"python list: {[optmized_sql_query, runtime_of_optimized_sql_query]} "\
                f"Don't write anything else"


    def field_with_description(self, type_, default_value, description):
        if default_value is ...:
            return (type_, Field(..., description=description))
        else:
            return (type_, Field(default_value, description=description))

    def get_fn_schema_from_fn_name(self, fn_name: str) -> Optional[Type[BaseModel]]:
        response = super().get_fn_schema_from_fn_name(fn_name)

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

            # print(f"getting schema for fn_name: {fn_name}")
            # print(f"response: {response.schema_json()}")

        return response

    def extract_schema(self, func_name):
        fn_schema = self.get_fn_schema_from_fn_name(func_name)
        return fn_schema

    def extract_func(self, func_name):
        func = getattr(self, func_name)
        return func
