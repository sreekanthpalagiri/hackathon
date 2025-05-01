from app.config import USE_LLM, GOOGLE_API_KEY, LLM_MODEL, EMBEDDING_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


def get_llm():
    if USE_LLM == "gemini":
        return ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)
    
def get_embedding_model():
    if USE_LLM == "gemini":
        return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)

