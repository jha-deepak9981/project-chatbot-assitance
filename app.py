# Complete Chatbot — Capstone Project
# ─────────────────────────────────────────────────────────
# COMPLETE AI CHATBOT — Module 3 Capstone Project
# ─────────────────────────────────────────────────────────

import streamlit as st
import google.generativeai as genai

# ── SETUP ──────────────────────────────────────────────────

api_key = st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    st.info("Enter your Gemini API key in the sidebar to start chatting.")
    st.stop()

genai.configure(api_key=api_key)

# The system prompt — sets the AI's personality and rules
SYSTEM_PROMPT = """You are Alex, a friendly and knowledgeable AI assistant.
You remember everything said earlier in this conversation.
If the user tells you their name, use it naturally in future responses.
Keep answers concise unless the user asks for detail.
If you don't know something, say so honestly."""

# Instantiate the Gemini model once with system instruction and generation config
model = genai.GenerativeModel(
    model_name="gemini-pro-latest",
    generation_config={
        "max_output_tokens": 1024,
        "temperature": 0.7
    },
    system_instruction=SYSTEM_PROMPT
)

# ── SESSION STATE ──────────────────────────────────────────
# Streamlit reruns the script on every interaction, so history lives in session_state
if "history" not in st.session_state:
    st.session_state.history = []

# ── CORE FUNCTION ──────────────────────────────────────────
def chat(user_input):
    """Send a message to Gemini and get a response, maintaining history."""

    st.session_state.history.append({"role": "user", "content": user_input})

    try:
        # Convert history format for Gemini API (roles 'user' and 'model')
        gemini_history = []
        for msg in st.session_state.history:
            gemini_role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": gemini_role, "parts": [{"text": msg["content"]}]})

        response = model.generate_content(contents=gemini_history)
        reply = response.text

        st.session_state.history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"Unexpected error: {str(e)}"

# ── UI ─────────────────────────────────────────────────────

st.title("Alex AI Chatbot")
st.caption("Powered by Gemini")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.history = []
    st.rerun()

# Display conversation history
for msg in st.session_state.history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])

# Chat input at the bottom
if user_input := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.write(user_input)

    reply = chat(user_input)

    with st.chat_message("assistant"):
        st.write(reply)
