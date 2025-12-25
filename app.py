import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Gemini Chatbot")
st.write("Chat with Google's Gemini model")

# Load API key securely
api_key = st.secrets.get("api_key")

if not api_key:
    st.error("API key not found. Please add GEMINI_API_KEY in Streamlit secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini response
    try:
        response = st.session_state.chat.send_message(user_input)
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
