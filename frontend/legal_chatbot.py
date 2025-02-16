import streamlit as st
import requests

# FastAPI Backend URL
API_URL = "https://law-chat-bot.onrender.com"  # Matching the backend endpoint

# Streamlit App UI
st.title("📜 Legal Study Chatbot")
st.write("Ask any legal question based on Indian Law.")

# Initialize session state for handling Enter key press
if "search_triggered" not in st.session_state:
    st.session_state["search_triggered"] = False

# Function to trigger search
def search():
    st.session_state["search_triggered"] = True

# Input for user query with Enter key functionality
query = st.text_input("Enter your legal question:", "", on_change=search, key="query_input")

# Button to trigger search
if st.button("Ask Chatbot") or st.session_state["search_triggered"]:
    st.session_state["search_triggered"] = False  # Reset flag after search
    if query.strip():
        with st.spinner("Fetching legal insights..."):
            try:
                response = requests.get(API_URL, params={"query": query})  # Matching the backend's query parameter
                if response.status_code == 200:
                    try:
                        data = response.json()  # Ensuring valid JSON response
                    except ValueError:
                        st.error("Invalid response from the server.")
                        st.stop()

                    st.subheader("🔍 Legal Explanation")
                    st.write(data)  # Since the backend directly returns the answer

                else:
                    st.error(f"API request failed with status code {response.status_code}.")

            except requests.RequestException as e:
                st.error(f"Request error: {e}")

    else:
        st.warning("Please enter a valid legal question.")
