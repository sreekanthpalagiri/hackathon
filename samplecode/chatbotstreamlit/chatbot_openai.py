import streamlit as st
import openai
import os

# Set your OpenAI API key from environment variable or directly here.
openai.api_key = os.environ.get("OPENAI_API_KEY")
# Alternatively:
# openai.api_key = "your-api-key-here"

# Function to get a response from the OpenAI ChatGPT REST API.
def get_chatgpt_response(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can change this to another model if preferred.
        messages=conversation,
        temperature=0.6,
    )
    return response['choices'][0]['message']['content']

# Initialize the conversation in session state.
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": "You are a helpful assistant."}]

st.title("ChatGPT Streamlit Chatbot")

# Display the conversation history
st.markdown("### Conversation")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**User:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Assistant:** {msg['content']}")
    else:
        # This will show system messages if needed.
        st.markdown(f"**System:** {msg['content']}")

# Input text-box for the user
user_input = st.text_input("Enter your message:")

if st.button("Send") and user_input:
    # Append the user message to the conversation history.
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Retrieve assistant's response via OpenAI REST API call.
    response = get_chatgpt_response(st.session_state.conversation)
    
    # Append the assistant's response to the conversation.
    st.session_state.conversation.append({"role": "assistant", "content": response})
    
    # Rerun the Streamlit script to update the conversation display.
    st.experimental_rerun()
