import asyncio

import os
import json

from pathlib import Path
from dotenv import load_dotenv
# Import the main customer service agent
from wise_owl.agent import wise_owl_agent

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

print("\nWise Owl Welcomes you!")
print("Type 'exit' or 'quit' to end the conversation.\n")



# ===== PART 2: Start Agent Session =====
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
        agent=wise_owl_agent,
        session_service=session_service,
    )

    # Set response modality = TEXT
    run_config = RunConfig(response_modalities=["TEXT"])

    return runner

'''async def agent_to_client_messaging(websocket, live_events):
    """Agent to client communication"""
    while True:
        async for event in live_events:
            # turn_complete
            if event.turn_complete:
                await websocket.send_text(json.dumps({"turn_complete": True}))
                print("[TURN COMPLETE]")

            if event.interrupted:
                await websocket.send_text(json.dumps({"interrupted": True}))
                print("[INTERRUPTED]")

            # Read the Content and its first Part
            part: Part = (
                event.content and event.content.parts and event.content.parts[0]
            )
            if not part or not event.partial:
                continue

            # Get the text
            text = event.content and event.content.parts and event.content.parts[0].text
            if not text:
                continue

            # Send the text to the client
            await websocket.send_text(json.dumps({"message": text}))
            print(f"[AGENT TO CLIENT]: {text}")
            await asyncio.sleep(0)


async def client_to_agent_messaging(websocket, live_request_queue):
    """Client to agent communication"""
    while True:
        text = await websocket.receive_text()
        content = Content(role="user", parts=[Part.from_text(text=text)])
        live_request_queue.send_content(content=content)
        print(f"[CLIENT TO AGENT]: {text}")
        await asyncio.sleep(0)'''

    
#
# FastAPI web app
#

app = FastAPI()

@app.get("/")
async def root():
    """Serves the index.html"""
    return 'Please use an endpoint'


@app.websocket("/ws/{user_name}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, user_name: str):
    """Client websocket endpoint"""

    # Wait for client connection
    await websocket.accept()
    print(f"Client #{session_id} connected for user {user_name}")

    # Start agent session
    if session_id:
        session_id = str(session_id)
        runner = start_agent_session(session_id, user_name)

        try:
            while True:
                user_input = await websocket.receive_text()

                print(user_input)
                
                add_user_query_to_history(
                    session_service, APP_NAME, user_name, session_id, user_input)
                # Process the received data (e.g., send to a service, transform, etc.)

                response_data = await call_agent_async(runner, user_name, session_id,  user_input)
                
                
                await websocket.send_text(response_data)
        except WebSocketDisconnect:
            # Handle client disconnection
            print("Client disconnected")