import streamlit as st
from typing import List
from api.dto.prompt_dto import HumanPromptDto, ConverseResponseDto
from api.ai.prompt_handler import handle_message
import time
from api.logging import logger

def log_elapsed_time(name: str, st: float, et: float):
    elapsed_time = et - st
    output = f"{name} Execution time: {'{:.2f}'.format(elapsed_time)} seconds"
    # if is_dev_env():
    #     print(output)
    logger.info(output)

def converse(dto: HumanPromptDto):
    st = time.time()
    response: ConverseResponseDto = handle_message(dto)
    et = time.time()
    logger.info(f"\n\n response from llm agent is: \n\n {response}\n\n")
    log_elapsed_time("converse", st, et)
    return response.response

# Streamlit app
def main():
    st.set_page_config(page_title="Amazing Chatbot UI", page_icon=":robot_face:", layout="wide")
    
    # Custom CSS for improved UI
    st.markdown("""
        <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
            padding: 10px;
            border-radius: 10px;
            background-color: #f5f5f5;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .chat-bubble {
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 10px;
            background-color: #007bff;
            color: white;
            text-align: left;
        }
        .chat-bubble.user {
            background-color: #6c757d;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Streamlit Chatbot for Radiologist")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Input area
    with st.form(key="chat_form"):
        user_input = st.text_input("You:", key="input")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        # Add user message to chat
        st.session_state.messages.append({"user": user_input})

        # Get chatbot response
        input = HumanPromptDto(message_id = "", consumer_id = "", prompt = user_input)
        response = converse(input)
        st.session_state.messages.append({"bot": response})

    # Display chat history
    if st.session_state.messages:
        with st.container():
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                if "user" in message:
                    st.markdown(f'<div class="chat-bubble user">{message["user"]}</div>', unsafe_allow_html=True)
                elif "bot" in message:
                    st.markdown(f'<div class="chat-bubble">{message["bot"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
