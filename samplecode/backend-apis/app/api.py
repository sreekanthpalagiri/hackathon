from fastapi import APIRouter
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from app.llm_provider import get_embedding_model, get_llm

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question

    # Load FAISS index using Gemini embeddings
    embeddings = get_embedding_model()
    
    print("Embeddings object created")

    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("Vectorstore loaded")

    docs = vectorstore.similarity_search(question, k=3)

    print("Similarity search completed")

    context = "\n".join(doc.page_content for doc in docs)

    print(f"Context is :", context)

    # Use Gemini LLM for response generation
    llm = get_llm()
    response = llm.invoke(f"Answer based on the following:\n{context}\n\n Ensure you reply from the given context only, else reply that I dont know.  \n\nQuestion: {question}")
    
    return {"answer": response}
