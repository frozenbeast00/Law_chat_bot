# from fastapi import FastAPI
# # import google.generativeai as genai
# from pydantic import BaseModel

# # Initialize FastAPI app

# # import requests

# # GOOGLE_SEARCH_API_KEY = "YOUR_GOOGLE_SEARCH_API_KEY"
# # SEARCH_ENGINE_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

# # def search_legal_sources(query):
# #     search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}"
# #     response = requests.get(search_url)
    
# #     if response.status_code == 200:
# #         results = response.json().get("items", [])
# #         return [item["link"] for item in results[:3]]  # Return top 3 sources
# #     return []
# # app = FastAPI()

# # # Set up Gemini API key
# # GEMINI_API_KEY = "AIzaSyDkpufO0bONKhFuoL0FhWYVl-pMQxiQdY0"
# # genai.configure(api_key=GEMINI_API_KEY)

# # # Define input model
# # class QueryRequest(BaseModel):
# #     query: str

# # @app.post("/query")
# # async def get_legal_answer(request: QueryRequest):
# #     try:
# #         model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
        
# #         # Enhance the prompt to make responses legally precise
# #         prompt = f"""
# #         You are a legal assistant for an LLB student in India. Your job is to provide highly accurate, 
# #         up-to-date information based on Indian laws, acts, and case laws. Answer the following study 
# #         question with legal reasoning and references:

# #         Question: {request.query}

# #         Ensure your response is structured and includes legal citations, case law (if applicable), and 
# #         references to Indian acts like IPC, CrPC, Constitution, etc.
# #         """

# #         response = model.generate_content(prompt)
# #         return {"answer": response.text}
    
# #     except Exception as e:
# #         return {"error": str(e)}

# # @app.post("/query")
# # async def get_legal_answer(request: QueryRequest):
# #     try:
# #         model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")

# #        prompt = f"""
# # You are an expert legal assistant specializing in Indian law, helping an LLB student prepare for exams. 
# # Your responses should be:

# # 1️⃣ **Legally Accurate**: Provide explanations using Indian laws, acts, and case laws.  
# # 2️⃣ **Cited & Referenced**: Include references to relevant acts, sections, and legal precedents.  
# # 3️⃣ **Concise & Structured**: Clearly explain key points in a simple yet professional manner.  
# # 4️⃣ **Exam-Oriented**: Answer in a way that helps the student grasp legal concepts easily.  

# # **Student's Question:**  
# # {request.query}  

# # ---

# # 📜 **Response Format:**  
# # ✅ **Legal Explanation:** (Define the legal principle)  
# # ✅ **Relevant Sections & Acts:** (Mention key laws, like IPC, CrPC, Constitution, etc.)  
# # ✅ **Case Law (if applicable):** (Reference a notable Supreme Court or High Court case)  
# # ✅ **Example (if needed):** (Provide a short example to illustrate the concept)  

# # Use clear, structured paragraphs without unnecessary fluff.  
# # """


# #         ai_response = model.generate_content(prompt)
        
# #         # Get legal sources
# #         legal_sources = search_legal_sources(request.query)
        
# #         return {
# #             "answer": ai_response.text,
# #             "sources": legal_sources
# #         }
    
# #     except Exception as e:
# #         return {"error": str(e)}

# import requests
# import google.generativeai as genai

# # API Keys (Replace with your own)
# SERPAPI_KEY = "f1aa12b63d908cb76cfccef7d34a5a710b1448bed2f8b716d6b4cfb737f3f847"  # Get from https://serpapi.com/
# GEMINI_API_KEY = "AIzaSyDkpufO0bONKhFuoL0FhWYVl-pMQxiQdY0"  # Get from Google AI Studio

# # Configure Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# # Function to perform web search using SerpAPI (Google)
# def google_search(query):
#     try:
#         url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}"
#         response = requests.get(url)
#         results = response.json()
        
#         # Extract the top 5 links
#         links = [item["link"] for item in results.get("organic_results", [])[:5]]
        
#         # If SerpAPI returns results, return them
#         if links:
#             print("Using Google Search (SerpAPI)")
#             return links
#     except Exception as e:
#         print("SerpAPI failed, falling back to DuckDuckGo:", e)
    
#     return None

# # Function to perform web search using DuckDuckGo (Backup)
# def duckduckgo_search(query):
#     try:
#         url = f"https://api.duckduckgo.com/?q={query}&format=json"
#         response = requests.get(url).json()

#         # Extract the top 5 links
#         links = [topic["FirstURL"] for topic in response.get("RelatedTopics", [])[:5] if "FirstURL" in topic]
        
#         if links:
#             print("Using DuckDuckGo API")
#             return links
#     except Exception as e:
#         print("DuckDuckGo API failed:", e)
    
#     return None

# # Function to get search results from either SerpAPI or DuckDuckGo
# def get_search_results(query):
#     links = google_search(query)
    
#     # If Google search fails, use DuckDuckGo
#     if not links:
#         links = duckduckgo_search(query)
    
#     return links if links else ["No relevant links found."]

# # Function to summarize search results using Gemini
# def summarize_content(links, query):
#     prompt = f"""
#     You are a highly knowledgeable legal assistant specializing in Indian law. Your task is to provide **accurate, concise, and well-structured legal summaries** based on the latest information from the web.

# ### **User Query:** "{query}"

# ### **Sources:**  
# {links}

# ### **Instructions:**  
# 1️⃣ **Extract only legally relevant information** from the sources.  
# 2️⃣ **Structure the response clearly** with appropriate headings.  
# 3️⃣ **Include legal provisions, acts, and case laws** when applicable.  
# 4️⃣ **Explain in a simple and easy-to-understand manner.**  

# ---

# ### **🔹 Response Format**
# **1️⃣ Legal Framework:**  
# - List relevant laws, sections, and acts.  
# - Mention case laws (if any).  
# - Provide citations if available.  

# **2️⃣ Key Legal Principles:**  
# - Summarize the fundamental legal concepts related to the query.  

# **3️⃣ Practical Implications:**  
# - Explain how the law is applied in real-world scenarios.  
# - Mention any recent legal changes (if applicable).  

# **4️⃣ Conclusion:**  
# - Provide a **direct, to-the-point answer** based on legal correctness.  
# - Avoid speculation or personal opinions.  
# """
#     try:
#         response = genai.generate_content(prompt)
#         return response.text if response else "Couldn't generate a summary."
#     except Exception as e:
#         print("Gemini API Error:", e)
#         return "Error while summarizing the content.
# # Function to get legal study help
# def get_legal_answer(query):
#     links = get_search_results(query)
#     summary = summarize_content(links, query)
    
#     return {
#         "query": query,
#         "sources": links,
#         "summary": summary
#     }

# # Example usage
# if __name__ == "__main__":
#     query = "What are the fundamental rights under Indian law?"
#     result = get_legal_answer(query)
    
#     print("\n🔹 Query:", result["query"])
#     print("\n🔹 Sources:", result["sources"])
#     print("\n🔹 Summary:\n", result["summary"])

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import google.generativeai as genai

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys (Replace with your own)
SERP_API_KEY = "f1aa12b63d908cb76cfccef7d34a5a710b1448bed2f8b716d6b4cfb737f3f847"  # Get from https://serpapi.com/
GEMINI_API_KEY = "AIzaSyDkpufO0bONKhFuoL0FhWYVl-pMQxiQdY0"  # Get from Google AI Studio

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)



# Optimized Prompt
LEGAL_PROMPT_TEMPLATE = """
You are a legal expert specializing in Indian law, including IPC, CrPC, the Constitution of India, and case laws. Your task is to provide a well-structured, informative, and up-to-date response to the following legal query.

    **User's Legal Question:**  
    {query}

    **Instructions for Answering:**  
    - First, provide a **detailed and structured legal explanation** based on your expert knowledge.
    - Cite relevant Indian legal provisions, acts, or precedents where applicable.
    - Use clear and concise language suitable for a law student or a professional seeking clarification.

    **Latest Legal Updates:**  
    Here are some recent articles or sources related to this topic:  
    {latest_updates}

    - Analyze these sources and summarize any relevant updates.
    - Highlight new amendments, Supreme Court/High Court rulings, or policy changes if applicable.
    - If no major updates exist, mention that the law remains unchanged.

    **Final Response Structure:**  
    1. **Legal Explanation** – Core answer based on Indian law.  
    2. **Latest Updates** – Summary of recent developments (if any).  
    3. **Reference Links** – List of sources for further reading.  

    Format your response professionally and ensure accuracy in legal interpretation.
    """
# Function to perform web search using SerpAPI (Google)
def google_search(query):
    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": f"{query} Indian law",
            "api_key": SERP_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        print("SerpAPI Response:", data)  # Debugging print
        if isinstance(data, dict) and "organic_results" in data:
            return [item["link"] for item in data["organic_results"][:5]]
    except Exception as e:
        print(f"SerpAPI failed: {e}")
    return []




# Function to perform web search using DuckDuckGo (Backup)
def duckduckgo_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query} Indian law&format=json"
        response = requests.get(url)
        data = response.json()
        print("DuckDuckGo Response:", data)  # Debugging print
        if isinstance(data, dict):
            return [entry["FirstURL"] for entry in data.get("RelatedTopics", []) if isinstance(entry, dict) and "FirstURL" in entry][:5]
    except Exception as e:
        print(f"DuckDuckGo failed: {e}")
    return []


INDIAN_LAW_KEYWORDS = [
    "Indian Penal Code", "IPC", "CrPC", "Constitution of India",
    "Supreme Court of India", "High Court", "Section", "Article", "Legal"
]

def filter_relevant_results(links):
    return [
        link for link in links if any(keyword.lower() in link.lower() for keyword in INDIAN_LAW_KEYWORDS)
    ][:5]

# Function to get search results from either SerpAPI or DuckDuckGo
def get_search_results(query):
    links = google_search(query)
    if not links:
        links = duckduckgo_search(query)
    return links if links else ["No relevant links found."]

# Function to summarize search results using Gemini
# Function to summarize search results using Gemini
def summarize_content(links, query):
    prompt = LEGAL_PROMPT_TEMPLATE.format(query=query, latest_updates="\n".join(links))
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")  # Ensure correct model usage
        response = model.generate_content(prompt)

        print("Gemini Response:", response)  # Debugging print

        # Ensure response is valid
        if response and hasattr(response, "text"):
            return response.text

        return "Couldn't generate a summary."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Error while summarizing the content."



# FastAPI Route: Handle chatbot queries 
@app.get("/ask")
async def ask_legal_chatbot(query: str = Query(..., title="Legal Query")):
    # links = get_search_results(query)
    # summary = summarize_content(links, query)
    latest_updates = get_search_results(query)  # Fetch latest news/articles
    response = summarize_content(query, latest_updates)
    print(f"""response:{response}""")
    return response

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Legal Study Chatbot API is running!"}
