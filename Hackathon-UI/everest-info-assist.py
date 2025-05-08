

import streamlit as st
# import os
from src.components.sidebar import render_sidebar
# from src.components.researcher import create_researcher, create_research_task, run_research
from src.utils.output_handler import capture_output
# import rest_api_util
import asyncio
import websockets
from uuid import uuid4

if "IS_RESPONSE_RECEIVED" not in st.session_state:
    st.session_state.IS_RESPONSE_RECEIVED = False


async def websocket_cient(message):
    uri = "wss://hackathon-backend-new-727170048524.us-central1.run.app:8080/ws/joydev/{}".format(uuid4())
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
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    #st.title(" :blue[Tenzing] :italic[- The Everest Agentic AI companion]", anchor=False)

    
# Define the HTML and CSS for the title
    title_html = """
        <style>
        .title {
            font-family: 'Arial', sans-serif;
            font-size: 100px;
            color: #215EF7;
            text-align: center;
        }
        </style>
        <h1 style="color:#215EF7;font-family:verdana;">Tenzing</h1>
        <p style="font-style:italic;font-family:verdana;font-size: 20px;">The Everest Agentic AI Companion</p>

    """
    print(title_html)
    # Use st.markdown to display the styled title
    st.markdown(title_html, unsafe_allow_html=True)



# Render sidebar and get selection (provider and model)
selection = render_sidebar()


# Create two columns for the input section
input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
with input_col2:
    message = st.text_area(
        "What would you like to know?",
        placeholder="Enter your querey here",
        height=68, 
        key = "message_text_area"
    )

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    start_search = st.button("🚀 Get Info", use_container_width=False, type="primary")
    result = ""
    url = "https://hackathon-authorization-727170048524.us-central1.run.app/items"
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
                    #response = 
                    if response:
                        st.markdown(response)
                        result = response
                        st.session_state.IS_RESPONSE_RECEIVED = True
                        status.update(label="✅ Information Retreived Successfully!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"An error occurred: {str(e)}")
                st.stop()
    
    # Convert AgentOutput to string for display and download
    result_text = str(result)
    
    # Display the final result
    st.markdown(result_text)


    # Create download buttons
    st.divider()
    download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
    with download_col2:
        st.markdown("### 📥 Download Conversation")
        
        # Download as Markdown
        st.download_button(
            label="Download the Conversation",
            data=result_text,
            file_name="conversation.md",
            mime="text/markdown",
            help="Download the conversation in Markdown format"
        )

# Create 8 columns for the follow-up section
if st.session_state.IS_RESPONSE_RECEIVED == True:
    input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
    with input_col2:
        task_description = st.text_area("",
            placeholder="Ask Follow Up....",
            height=68
        )

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 3, 1])
with footer_col2:
    st.caption("Empowered using Agentic AI Workflow, RAG and Prompt Engineering")