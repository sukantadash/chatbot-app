# config.py - Configuration Module

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    """
    Centralized configuration class for the application.
    Loads API credentials and model details from environment variables.
    """
    VLLM_API_URL = os.getenv("VLLM_API_URL")
    VLLM_API_KEY = os.getenv("VLLM_API_KEY")
    VLLM_MODEL_NAME = os.getenv("VLLM_MODEL_NAME", "default-vllm-model")

    # Raise an error early if critical configurations are missing
    if not VLLM_API_URL:
        raise ValueError("VLLM_API_URL environment variable is not set. Please set it in your .env file.")

    # You can add other global configurations here if needed
    DEFAULT_TEMPERATURE = 0.7
    SUMMARY_TEMPERATURE = 0.3
    CREATIVE_TEMPERATURE = 0.9
    CHAT_INITIAL_GREETING = "Hello! How can I assist you today?"

    # LLM response length limits for general chat vs. features
    MAX_TOKENS_CHAT = 200
    MAX_TOKENS_FEATURE = 250
