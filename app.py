# app.py - Main Application Entry Point

import gradio as gr
from config import AppConfig
from llm_service import LLMService
from ui import create_gradio_ui

# --- Initialize LLM Service ---
llm_service = LLMService()

# --- Gradio UI Logic ---
# app.py

def respond_to_chat(message, history):
    """
    Main function to handle user messages in the chatbot UI.
    """
    # If the user message is empty or None, just return the current state
    if not message:
        return "", history

    try:
        # Get response from the LLM service
        ai_response = llm_service.get_chat_response(message)

        # Gradio's 'messages' type for chatbot expects dictionaries
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": ai_response}
        ]
    except Exception as e:
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": f"Error processing chat: {e}. Please check server logs."}
        ]
    return "", new_history # Clear input, return updated history


# --- Create Gradio App ---
# Get the initial greeting from the LLM service
initial_greeting = llm_service.get_initial_greeting()

# Create the Gradio UI and assign it to the 'demo' variable at the global level
# This is CRITICAL for Uvicorn to find it.
demo = create_gradio_ui(
    respond_to_chat_fn=respond_to_chat,
    initial_greeting=initial_greeting
)

# The if __name__ == "__main__": block and demo.launch() are now REMOVED.
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)