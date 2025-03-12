import openai
import streamlit as st
import time

# OpenAI API Key
openai.api_key = ""
# Assistant ID
ASSISTANT_ID = ""

# Streamlit Page Config
st.set_page_config(page_title="Contra Coffee Chatbot", page_icon="☕", layout="wide")

# Initialize Session State
if "chats" not in st.session_state:
    st.session_state.chats = {}  # Stores all chat sessions
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "dropdown_open" not in st.session_state:
    st.session_state.dropdown_open = None  # Track which chat's dropdown is open


# Function to create a new chat
def new_chat():
    thread = openai.beta.threads.create()
    chat_id = thread.id
    st.session_state.chats[chat_id] = {"name": f"Chat {len(st.session_state.chats) + 1}", "messages": []}
    st.session_state.current_chat_id = chat_id
    st.rerun()


# Function to delete a chat
def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = None
        st.rerun()


# Function to rename a chat
def rename_chat(chat_id, new_name):
    if chat_id in st.session_state.chats:
        st.session_state.chats[chat_id]["name"] = new_name
        st.session_state.dropdown_open = None  # Close dropdown after renaming
        st.rerun()


# Function to load an existing chat
def load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    st.rerun()


# Sidebar Layout for Chat History
with st.sidebar:
    st.title("💬 Chat History")

    # New Chat Button
    if st.button("➕ New Chat", key="new_chat"):
        new_chat()

    # Display all saved chats
    for chat_id, chat_data in st.session_state.chats.items():
        col1, col2 = st.columns([4, 1])

        # Chat selection button
        if col1.button(chat_data["name"], key=f"select_{chat_id}"):
            load_chat(chat_id)

        # Three-dot dropdown menu
        with col2:
            if st.button("⋮", key=f"menu_{chat_id}"):
                if st.session_state.dropdown_open == chat_id:
                    st.session_state.dropdown_open = None  # Close dropdown
                else:
                    st.session_state.dropdown_open = chat_id  # Open dropdown
                st.rerun()

        # Show dropdown only for the clicked chat
        if st.session_state.dropdown_open == chat_id:
            with st.container():
                new_name = st.text_input("Rename chat:", value=chat_data["name"], key=f"rename_input_{chat_id}")
                if st.button(" Save", key=f"rename_confirm_{chat_id}"):
                    rename_chat(chat_id, new_name)

                if st.button(" Delete", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)

# Main Chat Interface
st.title("☕ Contra Coffee Chatbot")

if st.session_state.current_chat_id:
    chat_id = st.session_state.current_chat_id
    chat_data = st.session_state.chats[chat_id]

    # Display chat messages
    for msg in chat_data["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle user input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Save user message
        chat_data["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send message to OpenAI
        openai.beta.threads.messages.create(
            thread_id=chat_id,
            role="user",
            content=user_input
        )

        # Run assistant
        run = openai.beta.threads.runs.create(
            thread_id=chat_id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for assistant response
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=chat_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            time.sleep(1)

        # Retrieve assistant's response
        messages = openai.beta.threads.messages.list(thread_id=chat_id)
        assistant_response = messages.data[0].content[0].text.value

        # Save assistant response
        chat_data["messages"].append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

else:
    st.write("Start a new chat or select an existing conversation from the sidebar.")
