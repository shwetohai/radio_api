from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import time
from agent import build_agent
from pydantic import BaseModel
from typing import Optional, Union, Callable, List

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
    #human_id: str | None

class ConverseResponseDto(BaseModel):
    response: str


def handle_message(dto: HumanPromptDto):
    agent = build_agent()
    print(agent)
    res = agent.chat(dto.prompt)
    response = res.response
    print(f"\n\n agent result is \n\n {res.sources}\n\n")
    if response == "skip_response_to_the_user":
        response = ""
    return ConverseResponseDto(response = response)


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
    st = time.time()
    response: ConverseResponseDto = handle_message(dto)
    et = time.time()
    print(f"\n\n response from llm agent is: \n\n {response}\n\n")
    log_elapsed_time("converse", st, et)
    return response