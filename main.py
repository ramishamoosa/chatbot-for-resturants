import openai
import streamlit as st
import time


#  OpenAI API Key
openai.api_key = ""

#  Assistant ID
ASSISTANT_ID = ""

# Streamlit Page Config

st.set_page_config(page_title="Contra Coffee Chatbot", page_icon="☕", layout="wide")

st.title("Contra Coffe Chatbot")
#  Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores chat history
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()  # Creates a new OpenAI thread
    st.session_state.thread_id = thread.id

#  Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#  User Input Handling
user_input = st.chat_input("Type your message here...")

if user_input:
    #  Store User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    #  Send User Message to OpenAI Assistant
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    #  Run Assistant
    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=ASSISTANT_ID
    )

    #  Wait for Assistant's Response
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)  # Prevents rapid API polling

    #  Retrieve Assistant’s Response
    messages = openai.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )
    assistant_response = messages.data[0].content[0].text.value  # Gets latest message

    #  Display Assistant’s Response
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
