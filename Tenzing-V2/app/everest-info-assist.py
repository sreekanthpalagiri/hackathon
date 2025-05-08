

import streamlit as st
import os
from components.sidebar import render_sidebar
#import rest_api_util
import asyncio
import websockets
from uuid import uuid4
from main import websocket_endpoint

if "SESSION_ID" not in st.session_state:
    st.session_state.SESSION_ID = uuid4()

   
st.session_state.IS_RESPONSE_RECEIVED = False


session_id = st.session_state.SESSION_ID
print("Session Id : ", session_id)

async def websocket_cient(message):
    uri = "ws://127.0.0.1:8081/ws/June/{}".format(session_id)
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response

#--------------------------------#
#         Streamlit App          #
#--------------------------------#
# Configure the page
st.set_page_config(
    page_title="AI Agents as Subject Matter Expert",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Logo
st.logo(
    "everest_logo.png",
    size="large"
)

# Main layout
#col2, col3 = st.columns([1, 1])
#with col2:
    #st.title(" :blue[Tenzing] :italic[- The Everest Agentic AI Guide]", anchor=False)

# Define the HTML and CSS for the title
title_html = """<h1 style="color:#215EF7;font-family:verdana;">Tenzing</h1>  
    """

    # Use st.markdown to display the styled title
#st.markdown(title_html, unsafe_allow_html=True)

#with col3:
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("tenzing.png",width=200) 
    st.markdown(title_html, unsafe_allow_html=True)    

# Render sidebar and get selection (provider and model)
selection = render_sidebar()


# Create two columns for the input section
#input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
#with input_col2:
message = st.text_area(
    "",
    placeholder="Enter your query here",
    height=68, 
    key = "message_text_area"
)
download_col1, download_col2, download_col3 = st.columns([3, 6, 1])

with download_col3:
    start_search = st.button("🚀 Get Info", use_container_width=False, type="primary")

with download_col1:
    desc_html = """<h5 style='text-align: left;'>The Everest Agentic AI Companion</h5>"""
    st.markdown(desc_html, unsafe_allow_html=True)

result = ""
payload = message
if start_search:
    with st.status("🤖 Searching...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            #output_container = process_container.container()
            
            # Single output capture context.
            with process_container:
                response = asyncio.run(websocket_cient(payload))
                
                if response:
                    st.markdown(response)
                    result = response
                    st.session_state.IS_RESPONSE_RECEIVED = True
                    status.update(label="✅ Information Retrieved Successfully!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
    
    # Convert AgentOutput to string for display and download
result_text = str(result)



# Use st.markdown to display the styled title

#with input_col3:



# Display the final result
st.markdown(result_text)

# Create download buttons

# Create 8 columns for the follow-up section
if st.session_state.IS_RESPONSE_RECEIVED == True:
#input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
#with input_col2:
    task_description = st.text_area("",
        placeholder="Ask Follow Up....",
        height=68
    )

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 3, 1])
#with footer_col2:
st.caption("**Empowered using Agentic AI Workflow, RAG and Prompt Engineering**")