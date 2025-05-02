import streamlit as st
import anthropic

st.title("⬆️ Ingest Documents")

options = ["Upload a file", "Upload from ImageRight"]
selected_option = st.radio("Choose an action:", options,horizontal=True)

if selected_option == "Upload a file":
    uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
else:
    user_url = st.text_input("Enter a URL:")

st.button('Process')

