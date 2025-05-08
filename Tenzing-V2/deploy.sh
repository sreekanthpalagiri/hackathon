#!/bin/bash

# Start FastAPI server in background
uvicorn main:app --port 8081 &

# Start Streamlit server
streamlit run everest-info-assist.py --server.port 8080
