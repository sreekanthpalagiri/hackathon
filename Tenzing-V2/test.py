import streamlit as st
import asyncio
import websockets
 
async def websocket_client():
    uri = "ws://127.0.0.1:8081/ws/{}/{}".format('Sreekanth',12233)
    async with websockets.connect(uri) as websocket:
        await websocket.send("What is the approval and bind process")
        response = await websocket.recv()
        st.write(response)
        return response
 
st.title("WebSocket in Streamlit")
 
if st.button("Send Message"):
    response = asyncio.run(websocket_client())
 