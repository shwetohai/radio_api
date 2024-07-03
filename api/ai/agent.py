from typing import Any, Dict, List, Optional, Type
from dotenv import find_dotenv, load_dotenv
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from api.ai.tool import AllTool
from api.ai.prompts import SYSTEM_PROMPT

load_dotenv(find_dotenv())


def build_agent():

    FIELD_DESCRIPTIONS = {
        "upload_image": {},
        "my_availability": {},
        "talk_to_human_agent": {},
        "skip_response_to_the_user": {}
        #"talk_to_human_agent": {"sql_query": "Sql query"}
    }

    description_all = [
        "Use this when user wants to upload a image",
        "Use this when user wants to schedule their availability",
        "Use this when user wants to talk to a human agent",
        """Skip the response to the user

Use this function when you want to skip responding to the user.
This is useful when you don't want to sound repetetive or annoying.
This is also useful when the user sends a message that is not relevant to the conversation or when the user sends a message that is not actionable.
If you exectue this function no message will be sent to the user in response.
"""
    ]

    spec_functions = ["upload_image", "my_availability", "talk_to_human_agent", "skip_response_to_the_user"]

    reminder_tool = AllTool(
        FIELD_DESCRIPTIONS=FIELD_DESCRIPTIONS,
        spec_functions=spec_functions
    )

    tools_all = []
    for i in range(0, len(spec_functions)):
        try:
            #print(spec_functions[i])
            func_tool = reminder_tool.extract_func(spec_functions[i])
            #print(spec_functions[i])
            schema = reminder_tool.extract_schema(spec_functions[i])
            #print(spec_functions[i])
            #print("\n\n")
            #print(schema.schema())
            # print("\n\n")
            #print(spec_functions[i])
            # print(schema.model_json_schema())
            # print("\n\n")
            tool = FunctionTool.from_defaults(
                fn=func_tool,
                name=spec_functions[i],
                description=description_all[i],
                fn_schema=schema,
            )
            tools_all.append(tool)
        except Exception as e:
            print(e)
            continue

    llm = OpenAI(model="gpt-4o", temperature=0)
    agent = OpenAIAgent.from_tools(
        tools_all,
        llm=llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        # chat_history=history, #will add the getting history from database and also bring it in a format to be passed here in llama index agent
    )

    return agent
