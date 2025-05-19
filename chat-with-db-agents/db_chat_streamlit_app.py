import streamlit as st
from streamlit_chat import message
from db_chat_agent import db_chat_agent
from dotenv import load_dotenv
import os

# --- Load environment variables (.env) ---
load_dotenv()
st.set_page_config(page_title="Chat with your DB", page_icon="💬")

# --- Title and description ---
st.title("💬 DB Chat Agent")
st.markdown("Ask anything and the agent will talk to one or more database agents to get the answer. It will include the SQL and suggest follow-up steps!")

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat input ---
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append(("user", user_input))

    with st.spinner("Thinking..."):
        try:
            response = db_chat_agent.chat(user_input)
            if not isinstance(response, str):
                response = str(response)
        except Exception as e:
            response = f"❌ Error: {str(e)}"
        st.session_state.messages.append(("agent", response))

# --- Display messages as bubbles ---
for i, (sender, msg) in enumerate(st.session_state.messages):
    is_user = sender == "user"
    message(msg, is_user=is_user, key=str(i)) 