
import streamlit as st
import requests
import os
import time
# Base URL for the backend API
BASE_URL = "http://localhost:8000"  # Adjust based on deployment

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
                response = requests.get(f"{BASE_URL}/ask", params=params, timeout=15).json()
                
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