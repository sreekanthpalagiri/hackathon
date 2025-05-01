import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import CHUNK_SIZE, CHUNK_OVERLAP, GOOGLE_API_KEY, EMBEDDING_MODEL

def ingest_pdfs(folder_path: str, db_path: str = "faiss_index"):
    all_documents = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                path = os.path.join(root, file)
                loader = PyPDFLoader(path)
                all_documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(all_documents)

    # print(f"Total chunks: {len(chunks)}")
    # print(f"Google API Key", GOOGLE_API_KEY)

    # 🔁 Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,  
        google_api_key=GOOGLE_API_KEY
    )

    # 🧠 Create FAISS index
    vectorstore = FAISS.from_texts(
        [doc.page_content for doc in chunks],
        embedding=embeddings
    )
    vectorstore.save_local(db_path)

    print(f"Ingested {len(chunks)} chunks and saved FAISS DB at: {db_path}")
