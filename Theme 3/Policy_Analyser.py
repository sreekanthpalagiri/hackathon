from openai import OpenAI
import pandas as pd
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters


st.title("💬 Policy Language Analyser")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

st.sidebar.write('**Select The Policy Document** 👇')

df = pd.read_csv('./data/data.csv')

# display dynamic multi select filters
dynamic_filters = DynamicFilters(df, filters=['Doc Type', 'Document Name'])
dynamic_filters.display_filters(location='sidebar')
df_filtered = dynamic_filters.filter_df()

if st.sidebar.button("Load Document"):
    st.write("Button in the sidebar was clicked!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
