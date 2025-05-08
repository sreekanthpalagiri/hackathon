import streamlit as st

st.set_page_config(
    page_title="Tenzing",
    layout="wide", # Use wide layout for more space
    initial_sidebar_state="auto" # Keep sidebar visible initially
)
st.title("📰 An SME App to answer your questions in Everest")
st.markdown("""
Interact with an AI agent that can get answers for all thing in Everst Corporation.
**Examples:**
*   Ask for `latest news` (gets past 7 days).
*   Request `news from YYYY-MM-DD` (e.g., `news from 2024-04-10`).
*   Use `news from today` or `news from yesterday`.
*   After a briefing, ask follow-up questions like `tell me more about the first item` or `what was the link for the NPR story?` (The agent uses its memory!).
*(Note: News feed history is typically limited to ~2 weeks)*
""")
st.divider() # Add a visual separator

from dotenv import load_dotenv
# Import the main customer service agent
from tenzing.agent import tenzing_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

from google.genai.types import (
    Part,
    Content,
)

from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

# ===== PART 1: Initialize In-Memory Session Service and APP_NAME=====
session_service = InMemorySessionService()
APP_NAME = "Tenzing Backend"

def start_agent_session(session_id: str, user_name: str):
    """Starts an agent session"""

    print("Starts an agent session")
    print(session_service.get_session(
        app_name=APP_NAME,
        user_id=user_name,
        session_id=session_id))

    if  session_service.get_session(
        app_name=APP_NAME,
        user_id=user_name,
        session_id=session_id):

        session = session_service.get_session(
                app_name=APP_NAME,
                user_id=user_name,
                session_id=session_id)
    
    else:

        initial_state = {
        "user_name": user_name,
        "interaction_history": [],}

        # Create a Session
        session = session_service.create_session(
            app_name=APP_NAME,
            user_id=user_name,
            session_id=session_id,
            state=initial_state,
        )
        

    SESSION_ID = session.id
    print(f"Created new session: {SESSION_ID}")


    # Create a Runner
    runner = Runner(
        app_name=APP_NAME,
        agent=tenzing_agent,
        session_service=session_service,
    )

    # Set response modality = TEXT
    run_config = RunConfig(response_modalities=["TEXT"])

    return runner, SESSION_ID

try:
    adk_runner, SESSION_ID = start_agent_session('sreekanth', '12358')
    # Display initialization success and part of the session ID in the sidebar
    st.sidebar.success(f"ADK Initialized\nSession: ...{SESSION_ID}", icon="✅")
except Exception as e:
    # If ADK initialization fails (e.g., API error, configuration issue), display a critical error.
    st.error(f"**Fatal Error:** Could not initialize the ADK Runner or Session Service: {e}", icon="❌")
    st.error("Please check the terminal logs for more details, ensure your API key is valid, and restart the application.")
    st.stop() # Stop the app if ADK fails to initialize


# --- Chat Interface Implementation ---
# Use Streamlit's session state to store the chat message history.
# This makes the chat history persist across reruns of the script triggered by UI interactions.

message_history_key = "messages_final_mem_v2" # Use the same key consistently
if message_history_key not in st.session_state:
    # If no history exists for this session, initialize it as an empty list.
    st.session_state[message_history_key] = []
    print("Initialized Streamlit message history.")

for message in st.session_state[message_history_key]:
    # Use st.chat_message to render messages with appropriate icons (user/assistant).
    with st.chat_message(message["role"]):
        # Render message content using Markdown. Ensure HTML is not allowed for security.
        st.markdown(message["content"], unsafe_allow_html=False)

if prompt := st.chat_input("Ask for anything in Everest..."):
    print(f"User input received: '{prompt[:50]}...'")
    # 1. Append and display the user's message immediately.
    st.session_state[message_history_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=False)
    # 2. Process the user's prompt with the ADK agent and display the response.
    with st.chat_message("assistant"):
        # Use st.empty() as a placeholder to update with the full response later.
        # This gives a slightly better UX than just waiting and then showing the text.
        message_placeholder = st.empty()
        # Show a thinking indicator while the backend processes the request.
        with st.spinner("Assistant is thinking... (Fetching news if needed)"):
            try:
                # Call the synchronous wrapper function to run the ADK agent turn.
                add_user_query_to_history(
                    session_service, APP_NAME, 'Sreekanth', SESSION_ID,  prompt)
                # Process the received data (e.g., send to a service, transform, etc.)

                response_data = call_agent_async(adk_runner, 'Sreekanth', SESSION_ID,  prompt)
                # Update the placeholder with the agent's complete response.
                message_placeholder.markdown(response_data, unsafe_allow_html=False)
            except Exception as e:
                # If an error occurs during the ADK run, display it in the chat.
                error_msg = f"Sorry, an error occurred while processing your request: {e}"
                st.error(error_msg) # Show error prominently in the chat UI
                response_data = f"Error: Failed to get response. {e}" # Store simplified error in history
                
    # 3. Append the agent's response (or error message) to the chat history.
    st.session_state[message_history_key].append({"role": "assistant", "content": response_data})
    # Streamlit automatically reruns the script here, which redraws the chat history including the new messages.
    print("Agent response added to history. Streamlit will rerun.")

