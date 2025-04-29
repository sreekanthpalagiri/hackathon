import streamlit as st


st.header("Policy and Contract Validator")

# File uploader widget
uploaded_file = st.file_uploader("Upload your policy or contract file")

if uploaded_file is not None:
    # The uploaded file is now stored in the 'uploaded_file' variable
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    # You can now process the file as needed, for example:
    file_content = uploaded_file.read()
    st.write(file_content)
