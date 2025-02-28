# # # import streamlit as st
# # # import requests

# # # # FastAPI Backend URL
# # # API_URL = "https://law-chat-bot.onrender.com/ask"  # Matching the backend endpoint

# # # # Streamlit App UI
# # # st.title("📜 Legal Study Chatbot")
# # # st.write("Ask any legal question based on Indian Law.")

# # # # Initialize session state for handling Enter key press
# # # if "search_triggered" not in st.session_state:
# # #     st.session_state["search_triggered"] = False

# # # # Function to trigger search
# # # def search():
# # #     st.session_state["search_triggered"] = True

# # # # Input for user query with Enter key functionality
# # # query = st.text_input("Enter your legal question:", "", on_change=search, key="query_input")

# # # # Button to trigger search
# # # if st.button("Ask Chatbot") or st.session_state["search_triggered"]:
# # #     st.session_state["search_triggered"] = False  # Reset flag after search
# # #     if query.strip():
# # #         with st.spinner("Fetching legal insights..."):
# # #             try:
# # #                 response = requests.get(API_URL, params={"query": query})  # Matching the backend's query parameter
# # #                 if response.status_code == 200:
# # #                     try:
# # #                         data = response.json()  # Ensuring valid JSON response
# # #                     except ValueError:
# # #                         st.error("Invalid response from the server.")
# # #                         st.stop()

# # #                     st.subheader("🔍 Legal Explanation")
# # #                     st.write(data)  # Since the backend directly returns the answer

# # #                 else:
# # #                     st.error(f"API request failed with status code {response.status_code}.")

# # #             except requests.RequestException as e:
# # #                 st.error(f"Request error: {e}")

# # #     else:
# # #         st.warning("Please enter a valid legal question.")

# # # import streamlit as st
# # # import requests
# # # import io

# # # # Backend API URLs
# # # BACKEND_QUERY_URL = "https://law-chat-bot.onrender.com/ask"
# # # BACKEND_UPLOAD_URL = "https://your-backend-render-url.com/upload"

# # # st.title("Legal Study Chatbot 📜")

# # # # Document Upload Section
# # # st.subheader("📂 Upload Legal Documents")
# # # uploaded_file = st.file_uploader("Upload your legal documents (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# # # if uploaded_file:
# # #     with st.spinner("Uploading and processing document..."):
# # #         files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
# # #         response = requests.post(BACKEND_UPLOAD_URL, files=files)

# # #         if response.status_code == 200:
# # #             st.success("✅ Document uploaded successfully!")
# # #         else:
# # #             st.error("⚠️ Failed to upload document. Please try again.")

# # # st.markdown("---")

# # # # Legal Question Input
# # # st.subheader("💬 Ask a Legal Question")
# # # query = st.text_area("Enter your query:", placeholder="Type your legal question here...")

# # # if st.button("Get Answer"):
# # #     if query.strip():
# # #         with st.spinner("Fetching legal insights..."):
# # #             response = requests.get(BACKEND_QUERY_URL, params={"query": query})

# # #             if response.status_code == 200:
# # #                 data = response.json()

# # #                 # Extract response data
# # #                 answer = data.get("response", "No answer found.")
# # #                 retrieved_docs = data.get("retrieved_documents", [])
# # #                 sources = data.get("sources", [])

# # #                 # Display AI-generated Answer
# # #                 st.subheader("📌 Answer:")
# # #                 st.write(answer)

# # #                 # Display Retrieved Documents
# # #                 if retrieved_docs:
# # #                     st.subheader("📚 Retrieved from Uploaded Documents:")
# # #                     for i, doc in enumerate(retrieved_docs, 1):
# # #                         st.markdown(f"**{i}.** {doc}")

# # #                 # Display Web Sources
# # #                 if sources:
# # #                     st.subheader("🔗 Additional Web Sources:")
# # #                     for i, link in enumerate(sources, 1):
# # #                         st.markdown(f"[{i}. {link}]({link})")
# # #             else:
# # #                 st.error("⚠️ Failed to fetch response. Please try again.")

# # #     else:
# # #         st.warning("⚠️ Please enter a legal question.")


# # import streamlit as st
# # import requests

# # BASE_URL = "http://localhost:8000"  # Adjust based on deployment

# # st.title("Legal Study Bot 📜")

# # # Upload Section
# # st.header("Upload Legal Documents")
# # uploaded_file = st.file_uploader("Upload your legal document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# # if uploaded_file is not None:
# #     files = {"file": uploaded_file}
# #     upload_response = requests.post(f"{BASE_URL}/upload", files=files)
# #     st.success(upload_response.json().get("message", "Uploaded Successfully!"))

# # # Query Section
# # st.header("Ask a Legal Question")
# # query = st.text_input("Enter your legal question")

# # if st.button("Ask"):
# #     response = requests.get(f"{BASE_URL}/ask", params={"query": query}).json()
    
# #     st.subheader("Response:")
# #     st.write(response["response"])

# #     st.subheader("Sources Used:")
# #     st.write("\n".join(response["sources"]))

# #     st.subheader("Retrieved Documents:")
# #     st.write("\n".join(response["retrieved_documents"]))

# import streamlit as st
# import requests
# import time

# # Base URL for the backend API
# BASE_URL = "http://localhost:8000"  # Adjust based on deployment

# # Set page configuration for better appearance
# st.set_page_config(page_title="Legal Study Bot", page_icon="📜", layout="wide")

# # Title and description
# st.title("Legal Study Bot 📜")
# st.markdown("Upload legal documents and ask questions about Indian law. Get structured responses with legal explanations, updates, and references.")

# # Upload Section
# st.header("📤 Upload Legal Documents")
# uploaded_file = st.file_uploader(
#     "Upload your legal document (PDF, DOCX, TXT)", 
#     type=["pdf", "docx", "txt"], 
#     help="Supported formats: PDF, DOCX, TXT"
# )

# if uploaded_file is not None:
#     with st.spinner("Uploading document..."):
#         try:
#             files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
#             upload_response = requests.post(f"{BASE_URL}/upload", files=files, timeout=10)
#             upload_response.raise_for_status()  # Raise an error for bad status codes
#             st.success(upload_response.json().get("message", "Document uploaded successfully!"))
#         except requests.exceptions.RequestException as e:
#             st.error(f"Upload failed: {str(e)}")
#             if e.response is not None:
#                 st.write(f"Details: {e.response.text}")

# # Query Section
# st.header("❓ Ask a Legal Question")
# query = st.text_input("Enter your legal question", placeholder="e.g., What is IPC Section 302?", key="query_input")

# if st.button("Ask", key="ask_button"):
#     if not query.strip():
#         st.warning("Please enter a legal question.")
#     else:
#         with st.spinner("Fetching response..."):
#             try:
#                 response = requests.get(f"{BASE_URL}/ask", params={"query": query}, timeout=15).json()
                
#                 # Display Response
#                 st.subheader("📝 Generated Response")
#                 st.markdown(response.get("response", "No response generated."), unsafe_allow_html=True)

#                 # Display Sources
#                 st.subheader("🌐 Sources Used")
#                 sources = response.get("sources", [])
#                 if sources and sources != ["No relevant links found."]:
#                     for source in sources:
#                         st.markdown(f"- [{source}]({source})")
#                 else:
#                     st.write("No relevant sources found.")

#                 # Display Retrieved Documents
#                 st.subheader("📚 Retrieved Documents")
#                 retrieved_docs = response.get("retrieved_documents", [])
#                 if retrieved_docs:
#                     for i, doc in enumerate(retrieved_docs, 1):
#                         with st.expander(f"Document {i}", expanded=False):
#                             st.write(doc)
#                 else:
#                     st.write("No relevant documents retrieved.")

#             except requests.exceptions.RequestException as e:
#                 st.error(f"Failed to get response: {str(e)}")
#                 if e.response is not None:
#                     st.write(f"Details: {e.response.text}")
#             except ValueError:
#                 st.error("Invalid response format from server.")

# # Footer
# st.markdown("---")
# st.markdown("Built with ❤️ by Laksh Lalwani | Powered by FastAPI, Zilliz, and Gemini")
import streamlit as st
import requests
import os
import time
# Base URL for the backend API
# BASE_URL = "http://localhost:8000"
BASE_URL = "https://law-chat-bot.onrender.com"  # Adjust based on deployment

# Set page configuration
st.set_page_config(page_title="Legal Study Bot", page_icon="📜", layout="wide")

# Title and description
st.title("Legal Study Bot 📜")
st.markdown("Upload legal documents and ask questions about Indian law. Customize the importance of your documents vs. web search results.")

# Initialize session state for weights, upload message, and query
if "doc_weight" not in st.session_state:
    st.session_state.doc_weight = 50
if "web_weight" not in st.session_state:
    st.session_state.web_weight = 50
if "upload_message" not in st.session_state:
    st.session_state.upload_message = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = "file_uploader_0"
if "query_submitted" not in st.session_state:
    st.session_state.query_submitted = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# Upload Section
st.header("📤 Upload Legal Documents")
st.info("**Note:** Once a document is uploaded, it is stored in the database and does not need to be uploaded again unless you want to add new documents.")
uploaded_file = st.file_uploader(
    "Upload your legal document (PDF, DOCX, TXT)", 
    type=["pdf", "docx", "txt"], 
    help="Supported formats: PDF, DOCX, TXT",
    key=st.session_state.uploader_key
)

# Handle file selection and upload logic
if uploaded_file is not None:
    if st.button("Upload", key="upload_button"):
        with st.spinner("Uploading document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                upload_response = requests.post(f"{BASE_URL}/upload", files=files, timeout=10)
                upload_response.raise_for_status()
                file_name = uploaded_file.name
                st.session_state.upload_message = f"Successfully uploaded '{file_name}' to the database!"
                st.session_state.uploader_key = f"file_uploader_{time.time()}"
            except requests.exceptions.RequestException as e:
                st.session_state.upload_message = f"Upload failed: {str(e)}"
                if e.response is not None:
                    st.session_state.upload_message += f" Details: {e.response.text}"

# Display the upload message if it exists
if st.session_state.upload_message:
    if "Successfully uploaded" in st.session_state.upload_message:
        st.success(st.session_state.upload_message)
    else:
        st.error(st.session_state.upload_message)

# Query Section
st.header("❓ Ask a Legal Question")
query = st.text_input("Enter your legal question (press Enter to submit)", placeholder="e.g., What is IPC Section 302?", key="query_input")

# Weight Sliders with Synchronization
st.subheader("⚖️ Source Importance")
col1, col2 = st.columns(2)

def update_web_weight():
    """Update web_weight when doc_weight changes."""
    st.session_state.web_weight = 100 - st.session_state.doc_weight

def update_doc_weight():
    """Update doc_weight when web_weight changes."""
    st.session_state.doc_weight = 100 - st.session_state.web_weight

with col1:
    doc_weight = st.slider(
        "Uploaded Documents (%)",
        0,
        100,
        st.session_state.doc_weight,
        key="doc_weight_slider",
        on_change=update_web_weight
    )
with col2:
    web_weight = st.slider(
        "Internet Search (%)",
        0,
        100,
        st.session_state.web_weight,
        key="web_weight_slider",
        on_change=update_doc_weight
    )

# Ensure weights are synchronized
if doc_weight + web_weight != 100:
    st.session_state.web_weight = 100 - doc_weight
    st.rerun()

# Handle query submission on Enter or Ask button
def submit_query():
    st.session_state.query_submitted = True
    st.session_state.last_query = query

# Add Ask button as an alternative
st.button("Ask", key="ask_button", on_click=submit_query)

# Process query when Enter is pressed or Ask button is clicked
if (st.session_state.query_submitted and query != st.session_state.last_query) or (query and st.session_state.query_submitted):
    if not query.strip():
        st.warning("Please enter a legal question.")
        st.session_state.query_submitted = False
    else:
        with st.spinner("Fetching response..."):
            try:
                params = {"query": query, "doc_weight": doc_weight, "web_weight": web_weight}
                response = requests.get(f"{BASE_URL}/ask", params=params).json()
                
                st.subheader("📝 Generated Response")
                st.markdown(response.get("response", "No response generated."), unsafe_allow_html=True)

                st.subheader("🌐 Sources Used")
                sources = response.get("sources", [])
                if sources and sources != ["No relevant links found."]:
                    for source in sources:
                        st.markdown(f"- [{source}]({source})")
                else:
                    st.write("No relevant sources found.")

                st.subheader("📚 Retrieved Documents")
                retrieved_docs = response.get("retrieved_documents", [])
                if retrieved_docs:
                    for i, doc in enumerate(retrieved_docs, 1):
                        with st.expander(f"Document {i}", expanded=False):
                            st.write(doc)
                else:
                    st.write("No relevant documents retrieved.")

                st.subheader("⚖️ Weights Applied")
                st.write(f"Uploaded Documents: {response.get('doc_weight')}% | Internet Search: {response.get('web_weight')}%")

                # Reset query submission state after processing
                st.session_state.query_submitted = False
                st.session_state.last_query = query

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to get response: {str(e)}")
                if e.response is not None:
                    st.write(f"Details: {e.response.text}")
                st.session_state.query_submitted = False
            except ValueError:
                st.error("Invalid response format from server.")
                st.session_state.query_submitted = False

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Laksh | Powered by FastAPI, Zilliz, and Gemini")