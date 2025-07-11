# app.py - Main Application Entry Point

import gradio as gr
import os
from config import AppConfig
from llm_service import LLMService
from ui import create_gradio_ui

# --- Initialize LLM Service ---
# This will also load environment variables from .env via AppConfig
llm_service = LLMService()

# --- Gradio UI Logic ---

def respond_to_chat(message, history):
    """
    Main function to handle user messages in the chatbot UI.
    Delegates the LLM interaction to LLMService.
    `history` is Gradio's chat history: a list of dictionaries like
    {"role": "user", "content": "hello"}
    """
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


# --- Create and Launch Gradio App ---
if __name__ == "__main__":
    # Get the initial greeting from the LLM service (which gets it from config)
    initial_greeting = llm_service.get_initial_greeting()

    # Create the Gradio UI, passing only the required handler functions
    demo = create_gradio_ui(
        respond_to_chat_fn=respond_to_chat,
        initial_greeting=initial_greeting
    )

    # Launch the Gradio application.
    # share=True is required for environments where localhost is not accessible.
    # The frpc binary required for sharing is now included in the Containerfile.
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False
    )
