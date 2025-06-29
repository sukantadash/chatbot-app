# ui.py - Gradio User Interface

import gradio as gr
from config import AppConfig # Import configuration for initial greeting

# Custom CSS for styling the Gradio interface
CUSTOM_CSS = """
    /* Basic font styling, similar to Inter */
    body { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; }
    /* Custom styling for the chatbot interface */
    .gradio-container {
        max-width: 700px;
        margin: auto;
        border-radius: 12px; /* rounded-xl */
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1); /* shadow-2xl */
        border: 1px solid #E5E7EB; /* border-gray-200 */
        overflow: hidden;
    }
    .chat-header {
        background: linear-gradient(to right, #3B82F6, #8B5CF6); /* blue-600 to purple-600 */
        color: white;
        padding: 1rem;
        font-size: 1.25rem;
        font-weight: 600;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Custom message bubble styling in Gradio */
    .gradio-chatbot-message.bot {
        background-color: #E5E7EB !important; /* gray-200 */
        color: #374151 !important; /* gray-800 */
        border-radius: 0.5rem !important; /* rounded-lg */
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important; /* shadow-sm */
    }
    .gradio-chatbot-message.user {
        background-color: #3B82F6 !important; /* blue-500 */
        color: white !important;
        border-radius: 0.5rem !important; /* rounded-lg */
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important; /* shadow-sm */
    }
    /* Input and button styling in Gradio (often handled by theme, but can override) */
    .gr-button {
        border-radius: 9999px !important; /* rounded-full */
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .gr-button-primary {
        background-color: #3B82F6 !important; /* blue-600 */
        color: white !important;
    }
    .gr-button-primary:hover {
        background-color: #2563EB !important; /* blue-700 */
    }
    #summarize-btn.gr-button {
        background-color: #A78BFA !important; /* purple-500 */
    }
    #summarize-btn.gr-button:hover {
        background-color: #8B5CF6 !important; /* purple-600 */
    }
    #creative-btn.gr-button {
        background-color: #22C55E !important; /* green-500 */
    }
    #creative-btn.gr-button:hover {
        background-color: #16A34A !important; /* green-600 */
    }
    /* Hide settings button in Gradio toolbar */
    footer button[data-testid="SettingsButton"] {
        display: none !important;
    }

    /* Hide Gradio footer text like "Use via API" and "Built with Gradio" */
    footer {
        display: none !important;
    }
"""

def create_gradio_ui(respond_to_chat_fn, initial_greeting):
    """
    Creates and returns the Gradio Blocks interface for the chatbot.

    Args:
        respond_to_chat_fn: Function to handle user chat messages.
        initial_greeting: The initial message from the chatbot.

    Returns:
        gr.Blocks: The Gradio interface.
    """
    with gr.Blocks(
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS
        # Removed show_api, show_powered_by, show_settings from here.
        # These parameters are indeed only for the .launch() method, not gr.Blocks directly.
    ) as demo:
        gr.HTML('<div class="chat-header">AI Chatbot</div>')

        # Initial chatbot message (Gradio's 'messages' type expects dictionaries)
        initial_history = [{"role": "assistant", "content": initial_greeting}]

        # Chatbot component to display messages
        # Using type='messages' as recommended by Gradio UserWarning
        chatbot = gr.Chatbot(
            value=initial_history,
            height=400,
            show_copy_button=True,
            show_label=False,
            type='messages' # Set type to 'messages'
        )

        # Removed feature buttons and their row

        # User input and send button
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message...",
                show_label=False,
                container=False,
                scale=4
            )
            send_btn = gr.Button("Send", scale=1)

        # Event handlers for chat input
        msg.submit(respond_to_chat_fn, [msg, chatbot], [msg, chatbot])
        send_btn.click(respond_to_chat_fn, [msg, chatbot], [msg, chatbot])

    return demo
