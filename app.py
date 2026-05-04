# Complete Chatbot — Capstone Project
# ─────────────────────────────────────────────────────────
# COMPLETE AI CHATBOT — Module 3 Capstone Project
# ─────────────────────────────────────────────────────────

import os
import streamlit as st
import google.generativeai as genai

# ── SETUP ──────────────────────────────────────────────────

env_key = os.environ.get("GEMINI_API_KEY", "")
if env_key:
    api_key = env_key
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")

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

model = genai.GenerativeModel(
    model_name="gemini-pro-latest",
    generation_config={
        "max_output_tokens": 1024,
        "temperature": 0.7
    },
    system_instruction=SYSTEM_PROMPT
)

# ── SESSION STATE ──────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── CORE FUNCTION ──────────────────────────────────────────
def chat(user_input):
    st.session_state.history.append({"role": "user", "content": user_input})

    try:
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

# ── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    if env_key:
        st.success("API key loaded from environment.")

    st.markdown("### Conversation History")
    if st.session_state.history:
        for msg in st.session_state.history:
            label = "You" if msg["role"] == "user" else "Alex"
            with st.expander(f"{label}: {msg['content'][:40]}..."):
                st.write(msg["content"])
    else:
        st.write("No history yet.")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    with col2:
        if st.button("Reset", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ── MAIN UI ────────────────────────────────────────────────
st.title("Alex AI Chatbot")
st.caption("Powered by Gemini")

for msg in st.session_state.history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])

if user_input := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.write(user_input)

    reply = chat(user_input)

    with st.chat_message("assistant"):
        st.write(reply)
