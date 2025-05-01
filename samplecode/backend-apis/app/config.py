from dotenv import load_dotenv
import os

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "gemini").lower()
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash-001")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
