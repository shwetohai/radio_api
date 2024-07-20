import os
from typing import Any, Dict, List, Optional, Type

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from llama_index.agent.openai.base import OpenAIAgent
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.llms.openai import OpenAI
import copy
from prompts import SYSTEM_PROMPT
from tool import DoctorTool
from llama_index.core.bridge.pydantic import BaseModel

load_dotenv(find_dotenv())


class ToolSpec(BaseModel):
    # this is the type of tool that will be instantiated, it is NOT an instance of the tool
    tool_type: Any


class IntentContext(BaseModel):
    """"""

    tool_specs: Optional[List[ToolSpec]] = []


def get_history():
    chat_messages: List[ChatMessage] = []
    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")

        type = df["type"].tolist()
        message = df["message"].tolist()
        tool = df["tool"].tolist()
        for i in range(0, len(message)):
            if type[i] == "user":
                chat_messages.append(
                    ChatMessage(role=MessageRole.USER, content=message[i])
                )
            elif type[i] == "function":
                chat_messages.append(
                    ChatMessage(
                        role=MessageRole.FUNCTION,
                        content=message[i],
                        additional_kwargs={"name": tool[i]},
                    )
                )

            else:
                chat_messages.append(
                    ChatMessage(role=MessageRole.ASSISTANT, content=message[i])
                )
    print(chat_messages[-20:])

    return chat_messages[-20:]



def get_history_from_sql():
    pass

def build_agent():

    doctor_tool = ToolSpec(tool_type=DoctorTool)
    all_tools: List[ToolSpec] = [doctor_tool]

    TOOL_TABLE = {
        "unclassified": IntentContext(tool_specs=all_tools),
    }

    available_tools = copy.deepcopy(TOOL_TABLE["unclassified"])

    tools: List[ToolSpec] | None = []
    for tool_spec in available_tools.tool_specs:
        tool = tool_spec.tool_type()
        tools.extend(tool.to_tool_list())

    llm = OpenAI(model="gpt-4o", temperature=0)
    agent = OpenAIAgent.from_tools(
        tools,
        llm=llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        chat_history=get_history(),
        # chat_history=history, #will add the getting history from database and also bring it in a format to be passed here in llama index agent
    )
    return agent
