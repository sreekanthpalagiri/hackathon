import streamlit as st
import requests

def get_system_message():
    """Fetch system message from REST API"""
    try:
        response = requests.get("https://api.example.com/system-message")
        return response.json()["message"]
    except Exception as e:
        return "Default system message: How can I help you?"

# Initialize chat history with system message
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Get system message and add as first message
    system_msg = get_system_message()
    st.session_state.messages.append({"role": "assistant", "content": system_msg})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate bot response (simple echo for demonstration)
    bot_response = f"Echo: {prompt}"
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
