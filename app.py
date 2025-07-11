# app.py - Main Application Entry Point

import gradio as gr
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

    # Launch the Gradio application
    # Set server_name to "0.0.0.0" to bind to all interfaces, making it accessible from outside the container
    # Set server_port to 7860 to use the standard port
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_api=False
    )
