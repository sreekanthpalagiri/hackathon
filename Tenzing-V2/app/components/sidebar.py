import streamlit as st
import os
import requests
import emoji


#--------------------------------#
#      Sidebar Configuration     #
#--------------------------------#
def render_sidebar():
    """Render the sidebar 
    """
    with st.sidebar:
        st.markdown(':man: Hi John,')
        st.markdown("Welcome!...... " \
        "We can help you with your query per information available with us as of today from Everest")
        
        with st.expander("ℹ️ Tips", expanded=True):
            st.markdown("""
                This Agentic AI Subject Matter Experts use advanced Agentic AI architecture to help you:
                - Access particular/contextual information from documents/database/systems per user's access privilege 
                - Ask me about early office closings for your country 
                - I can also provide you information on certain applications, like what does EZFlow do? 
                - Looking for procedural information? Ask me how to resubmit a claim in EZFlow. 
                - I'll summarize emails for a client in EZFlow 
                - Is the terrorism exception clause for a client?                        
            """)
   