import time
from typing import Callable, List, Optional, Union

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import build_agent

app = FastAPI(title="Radiologist Agent API", version="0.1.0" )

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

# Include the router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8111)