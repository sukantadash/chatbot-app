# app.py - Streamlit Chatbot Application

import streamlit as st
from llm_service import LLMService

# --- App Title ---
st.title("AI Chatbot")

# --- Initialize LLM Service ---
# This will also load environment variables from .env via AppConfig
# and initialize the conversation chain.
llm_service = LLMService()

# --- Initialize Chat History in Session State ---
# For more information on session state, see:
# https://docs.streamlit.io/library/api-reference/session-state
if "messages" not in st.session_state:
    # Start with the initial greeting from the assistant
    initial_greeting = llm_service.get_initial_greeting()
    st.session_state.messages = [{"role": "assistant", "content": initial_greeting}]

# --- Display Prior Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
# The st.chat_input widget will automatically rerun the app on submission
if prompt := st.chat_input("What would you like to talk about?"):
    # 1. Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get AI response and display it
    with st.chat_message("assistant"):
        # Use a placeholder for the streaming effect
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Get response from the LLM service
            ai_response = llm_service.get_chat_response(prompt)
            full_response = ai_response
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Error processing chat: {e}. Please check server logs."
            message_placeholder.markdown(full_response)
    
    # 3. Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# To run this app:
# 1. Make sure you have an active virtual environment.
# 2. Ensure your .env file is correctly configured.
# 3. Run `streamlit run app.py` in your terminal.
