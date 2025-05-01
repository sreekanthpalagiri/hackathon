from fastapi import FastAPI
from app.api import router

app = FastAPI(title="RAG API with LangChain & FAISS")

app.include_router(router, prefix="/api")
