from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from api.dto.prompt_dto import HumanPromptDto, ConverseResponseDto
from api.ai.prompt_handler import handle_message
import time
from api.logging import logger

router = APIRouter(
    prefix="/taskproof",
    tags=["llm"],
    responses={404: {"description": "Not found"}},
)

def log_elapsed_time(name: str, st: float, et: float):
    elapsed_time = et - st
    output = f"{name} Execution time: {'{:.2f}'.format(elapsed_time)} seconds"
    # if is_dev_env():
    #     print(output)
    logger.info(output)

@router.post("/converse")
def converse(dto: HumanPromptDto) -> ConverseResponseDto:
    st = time.time()
    response: ConverseResponseDto = handle_message(dto)
    et = time.time()
    logger.info(f"\n\n response from llm agent is: \n\n {response}\n\n")
    log_elapsed_time("converse", st, et)
    return response.dict()