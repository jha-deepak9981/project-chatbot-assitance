# Complete Chatbot — Capstone Project
# ─────────────────────────────────────────────────────────
# COMPLETE AI CHATBOT — Module 3 Capstone Project
# ─────────────────────────────────────────────────────────
# pip install google-generativeai # Changed: Install Google Generative AI library

import google.generativeai as genai # Changed: Import Google Generative AI

# ── SETUP ──────────────────────────────────────────────────
#from google.colab import userdata # Keep this for Colab secrets

import streamlit as st
api_key = st.secrets["gemini_api_key"]
genai.configure(api_key=api_key) # Changed: Configure Gemini API

# Conversation history — list of dictionaries
# Each message: {"role": "user" or "assistant", "content": "text"}
history = []

# The system prompt — sets the AI's personality and rules
SYSTEM_PROMPT = """You are Alex, a friendly and knowledgeable AI assistant.
You remember everything said earlier in this conversation.
If the user tells you their name, use it naturally in future responses.
Keep answers concise unless the user asks for detail.
If you don't know something, say so honestly."""

# Instantiate the Gemini model once with system instruction and generation config
model = genai.GenerativeModel(
    model_name="gemini-pro-latest", # Using gemini-pro as a stable model
    generation_config={
        "max_output_tokens": 1024, # Maximum length of response (in tokens)
        "temperature": 0.7         # Creativity level (0=factual, 1=creative)
    },
    system_instruction=SYSTEM_PROMPT # Set system instruction here
)

# ── CORE FUNCTION ──────────────────────────────────────────
def chat(user_input):
    """Send a message to Gemini and get a response, maintaining history."""

    # 1. Add the user's message to history
    history.append({
        "role": "user",
        "content": user_input
    })

    # 2. Call the API with the FULL history (so AI remembers everything)
    try:
        # Convert history format for Gemini API (roles 'user' and 'model')
        gemini_history = []
        for msg in history:
            gemini_role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": gemini_role, "parts": [{"text": msg["content"]}]})

        response = model.generate_content(
            contents=gemini_history
        )

        # 3. Extract the reply text
        reply = response.text # Changed: Gemini response parsing

        # 4. Add AI's reply to history (so it's remembered next turn)
        history.append({
            "role": "assistant", # Keep 'assistant' for internal consistency
            "content": reply
        })

        return reply

    except Exception as e: # General exception handling for Gemini errors
        # You can add more specific Gemini API exception handling if needed
        return f"Unexpected error: {str(e)}"

# ── UTILITY FUNCTIONS ──────────────────────────────────────
def show_history():
    """Print the full conversation history."""
    print("""
─── Conversation History ───""")
    for i, msg in enumerate(history):
        label = "You" if msg["role"] == "user" else "Alex"
        print(f"{label}: {msg['content'][:100]}...")  # Truncate for display
    print("""───────────────────────────
""")

def clear_memory():
    """Clear the conversation history."""
    history.clear()
    print("""Memory cleared! Starting fresh.
""")

# ── MAIN LOOP ──────────────────────────────────────────────
def main():
    print("Alex AI Chatbot (powered by Gemini)") # Changed: Update chatbot name
    print("Commands: 'quit' to exit | 'history' to see conversation | 'clear' to reset")
    print("─" * 60)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Handle empty input
        if not user_input:
            continue

        # Handle special commands
        if user_input.lower() == "quit":
            print("Goodbye! Thanks for chatting with Alex.")
            break
        elif user_input.lower() == "history":
            show_history()
            continue
        elif user_input.lower() == "clear":
            clear_memory()
            continue

        # Send to AI and print response
        response = chat(user_input)
        print(f"\nAlex: {response}")

# Run the chatbot
if __name__ == "__main__":
    main()

