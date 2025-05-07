import streamlit as st
import os
import requests
import emoji

#--------------------------------#
#      Ollama Integration        #
#--------------------------------#
def get_ollama_models():
    """Get list of available Ollama models from local instance.
    
    Returns:
        list: Names of available Ollama models, or empty list if Ollama is not running
    """
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            return [model["name"] for model in models["models"]]
        return []
    except:
        return []

#--------------------------------#
#      Sidebar Configuration     #
#--------------------------------#
def render_sidebar():
    """Render the sidebar 
    """
    with st.sidebar:
        st.markdown(':man: Hi John,')
        st.write("Welcome!...... " \
        "we can help you with your query per your current access privilege and information available with us as of today from Everest Global")
        
        with st.expander("ℹ️ Special Note", expanded=False):
            st.markdown("""
                This Agentic AI Subject Matter Experts use advanced Agentic AI architecture to help you:
                - Find generic information for employees  
                - Access particular/contextual information from documents/database/systems per user's access privilege 
                - Redirect users to specific contacts for help in case information not available     
            """)
   