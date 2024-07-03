from api.ai.agent import build_agent
from api.dto.prompt_dto import HumanPromptDto, ConverseResponseDto


def handle_message(dto: HumanPromptDto):
    agent = build_agent()
    print(agent)
    res = agent.chat(dto.prompt)
    response = res.response
    if response == "skip_response_to_the_user":
        response = ""
    return ConverseResponseDto(response = response)
