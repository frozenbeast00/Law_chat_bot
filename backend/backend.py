

from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import google.generativeai as genai
import os
import shutil
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from typing import List
from pdfminer.high_level import extract_text
from docx import Document

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys
SERP_API_KEY = "f1aa12b63d908cb76cfccef7d34a5a710b1448bed2f8b716d6b4cfb737f3f847"
GEMINI_API_KEY = "AIzaSyDkpufO0bONKhFuoL0FhWYVl-pMQxiQdY0"
ZILLIZ_URI = "https://in03-e7edad095807c90.serverless.gcp-us-west1.cloud.zilliz.com"
ZILLIZ_API_KEY = "6931c71bdd824b8e440a8f33593f4f25202a10da2c26edbed346fb390f99c3631725b921d6472e138f568b65605e804b4eed9d23"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Connect to Zilliz Cloud
connections.connect(alias="default", uri=ZILLIZ_URI, token=ZILLIZ_API_KEY)

# Initialize Embedding Model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIM = 384  # Dimension of all-MiniLM-L6-v2 embeddings

# Legal Prompt Template
LEGAL_PROMPT_TEMPLATE = """
You are a legal expert specializing in Indian law, including IPC, CrPC, the Constitution of India, and case laws. Your task is to provide a well-structured, informative, and up-to-date response to the following legal query.

    **User's Legal Question:**  
    {query}

    **Instructions for Answering:**  
    - Provide a **detailed and structured legal explanation** based on your expert knowledge.
    - Cite relevant Indian legal provisions, acts, or precedents where applicable.
    - Use clear and concise language suitable for a law student or a professional seeking clarification.
    - Weigh the importance of the following sources as per user preference:
      - Uploaded Documents: {doc_weight}%
      - Internet Search: {web_weight}%

    **Context from Uploaded Documents ({doc_weight}% importance):**  
    {context}

    **Latest Legal Updates from Internet Search ({web_weight}% importance):**  
    {latest_updates}

    **Final Response Structure:**  
    1. **Legal Explanation** – Core answer based on Indian law, balancing the weighted sources.
    2. **Latest Updates** – Summary of recent developments (if any).
    3. **Reference Links** – List of sources for further reading.

    Format your response professionally and ensure accuracy in legal interpretation.
"""

# Create or Load Zilliz Collection
def initialize_collection():
    collection_name = "legal_docs"
    if not utility.has_collection(collection_name):
        schema = CollectionSchema(
            fields=[
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
            ],
            description="Legal Documents Collection"
        )
        collection = Collection(name=collection_name, schema=schema)
        collection.create_index(
            field_name="embedding",
            index_params={"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 1024}}
        )
        print(f"✅ Created collection: {collection_name}")
    else:
        collection = Collection(name=collection_name)
        print(f"✅ Loaded existing collection: {collection_name}")
    collection.load()
    return collection

# Initialize collection at startup
collection = initialize_collection()

# Function to Extract Text from Files
def extract_text_from_file(file_path: str) -> str:
    ext = file_path.split(".")[-1].lower()
    try:
        if ext == "pdf":
            return extract_text(file_path)
        elif ext == "docx":
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type: pdf, docx, txt only")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
    return ""

# Upload and Ingest Document
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = f"temp_files/{file.filename}"
    os.makedirs("temp_files", exist_ok=True)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        content = extract_text_from_file(file_path)
        if not content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the document.")
        
        embedding = embedding_model.encode(content).tolist()
        collection.insert([[content], [embedding]])
        return {"message": "Document uploaded and stored in Zilliz successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Retrieve Documents from Zilliz
def retrieve_documents(query: str, top_k: int = 5) -> List[str]:
    try:
        query_embedding = embedding_model.encode(query).tolist()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        search_results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["content"]
        )
        return [hit.entity.get("content", "") for hit in search_results[0]]
    except Exception as e:
        print(f"Document Retrieval Error: {e}")
        return []

# Web Search
INDIAN_LAW_KEYWORDS = ["Indian Penal Code", "IPC", "CrPC", "Constitution of India", "Supreme Court"]

def google_search(query: str) -> List[str]:
    try:
        url = "https://serpapi.com/search"
        params = {"engine": "google", "q": f"{query} Indian law", "api_key": SERP_API_KEY}
        response = requests.get(url, params=params).json()
        return [item["link"] for item in response.get("organic_results", [])][:5]
    except Exception as e:
        print(f"Google Search Error: {e}")
        return []

def filter_relevant_results(links: List[str]) -> List[str]:
    return [link for link in links if any(keyword.lower() in link.lower() for keyword in INDIAN_LAW_KEYWORDS)][:5]

def get_search_results(query: str) -> List[str]:
    links = google_search(query)
    filtered_links = filter_relevant_results(links)
    return filtered_links if filtered_links else ["No relevant links found."]

# Summarize Content with Gemini
def summarize_content(query: str, retrieved_docs: List[str], latest_updates: List[str], doc_weight: float, web_weight: float) -> str:
    context = "\n\n".join(retrieved_docs) if retrieved_docs else "No stored documents found."
    sources = "\n".join(latest_updates) if latest_updates else "No external sources found."
    prompt = LEGAL_PROMPT_TEMPLATE.format(
        query=query,
        doc_weight=doc_weight,
        web_weight=web_weight,
        context=context,
        latest_updates=sources
    )
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else "Couldn't generate a summary."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Error summarizing content."

# Chatbot API with Weight Parameters
@app.get("/ask")
async def ask_legal_chatbot(
    query: str = Query(..., title="Legal Query"),
    doc_weight: float = Query(50.0, ge=0.0, le=100.0, title="Weight for Uploaded Documents (%)"),
    web_weight: float = Query(50.0, ge=0.0, le=100.0, title="Weight for Internet Search (%)")
):
    # Ensure weights sum to 100%
    total_weight = doc_weight + web_weight
    if total_weight != 100.0:
        raise HTTPException(status_code=400, detail="Weights must sum to 100%.")
    
    latest_updates = get_search_results(query)
    retrieved_docs = retrieve_documents(query)
    response = summarize_content(query, retrieved_docs, latest_updates, doc_weight, web_weight)
    return {
        "query": query,
        "sources": latest_updates,
        "retrieved_documents": retrieved_docs,
        "response": response,
        "doc_weight": doc_weight,
        "web_weight": web_weight
    }

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Legal Study Chatbot API is running!"}