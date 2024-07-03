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