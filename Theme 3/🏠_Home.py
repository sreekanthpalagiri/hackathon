from openai import OpenAI
import pandas as pd
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters


st.title("💬 Policy Language Analyser")
st.caption("🚀 Please load the document to see LLM analysis.")


for i in range(17):
    st.sidebar.write(" ")

st.sidebar.divider()
st.sidebar.write('**Select The Policy Document** 👇')
df = pd.read_csv('./data/data.csv')
# display dynamic multi select filters
dynamic_filters = DynamicFilters(df, filters=['Doc Type', 'Document Name'])
dynamic_filters.display_filters(location='sidebar')
df_filtered = dynamic_filters.filter_df()

if st.sidebar.button("Load Document"):
    st.write("Button in the sidebar was clicked!")

st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Talk to your document"):
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
