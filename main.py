import os
import time
from typing import Callable, List, Optional, Union

import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import build_agent

app = FastAPI(title="Radiologist Agent API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConsumerPromptDto(BaseModel):
    """this is the end user of the application"""

    message_id: str
    consumer_id: str
    prompt: str
    # exchange_id: Optional[str] = None
    # household_member_id: str
    # household_id: str


class HumanPromptDto(ConsumerPromptDto):
    """this is the EA"""
    # human_id: str | None


class ConverseResponseDto(BaseModel):
    response: str
    success: bool
    error: str
    type: List[str]


def extract_functions(functions):
    tool = []
    if functions:
        for i in functions:
            tool.append(i.tool_name)
    return tool


def save_history(user_message, bot_message, functions):
    message = []
    type_ = []  # type is a reserved keyword, so use type_ instead
    tool = []
    message.append(user_message)
    type_.append("user")
    tool.append("")
    if functions:
        for i in functions:
            message.append(i.content)
            type_.append("function")
            tool.append(i.tool_name)
    message.append(bot_message)
    type_.append("bot")
    tool.append("")

    # Create a DataFrame from the data
    data = pd.DataFrame({"message": message, "type": type_, "tool": tool})

    if os.path.exists("data.csv"):
        # If the file exists, append the new data
        data.to_csv("data.csv", mode="a", header=False, index_label="id")
    else:
        # If the file does not exist, create it with headers
        data.to_csv("data.csv", mode="w", header=True, index_label="id")


def handle_message(dto: HumanPromptDto):
    try:
        agent = build_agent()
        print(agent)
        print(dto.prompt)
        res = agent.chat(dto.prompt)
        response = res.response
        print(f"\n\n agent chat history is \n\n {agent.chat_history}\n\n")
        print(f"\n\n agent result is \n\n {res.sources}\n\n")
        if response == "skip_response_to_the_user" or response == "":
            response = "Currently I am in Beta. I can help you with user schedule, upload image and assist with talking to human agent"
        save_history(dto.prompt, response, res.sources)
        tools = extract_functions(res.sources)
        return response, tools
    except Exception as e:
        print(e)
        return "", ""


router = APIRouter(
    prefix="/taskproof",
    tags=["llm"],
    responses={404: {"description": "Not found"}},
)


def log_elapsed_time(name: str, st: float, et: float):
    elapsed_time = et - st
    output = f"{name} Execution time: {'{:.2f}'.format(elapsed_time)} seconds"
    print(output)


@router.post("/converse")
def converse(dto: HumanPromptDto) -> ConverseResponseDto:
    try:
        st = time.time()
        response, tools = handle_message(dto)
        et = time.time()
        print(f"\n\n response from llm agent is: \n\n {response}\n\n")
        log_elapsed_time("converse", st, et)
        return ConverseResponseDto(
            response=response, error="", success=True, type=tools
        )
    except Exception as e:
        return ConverseResponseDto(response="", error=str(e), success=False, type=[])


# Include the router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
