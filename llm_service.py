# llm_service.py - LLM Interaction Service

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from config import AppConfig # Import configuration

class LLMService:
    """
    Manages all interactions with the LLM model using LangChain.
    Encapsulates LLM initialization, conversation memory, and prediction logic.
    """
    def __init__(self):
        """
        Initializes the LLM and the main conversation chain.
        """
        self.llm = ChatOpenAI(
            model_name=AppConfig.VLLM_MODEL_NAME,
            openai_api_base=AppConfig.VLLM_API_URL,
            openai_api_key=AppConfig.VLLM_API_KEY,
            temperature=AppConfig.DEFAULT_TEMPERATURE
        )
        # LangChainDeprecationWarning: Please see the migration guide at: https://python.langchain.com/docs/versions/migrating_memory/
        self.memory = ConversationBufferMemory(return_messages=True)
        # LangChainDeprecationWarning: The class `ConversationChain` was deprecated in LangChain 0.2.7 and will be removed in 1.0. Use :class:`~langchain_core.runnables.history.RunnableWithMessageHistory` instead.
        self.conversation_chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )

        # Initialize memory with the initial greeting for the chatbot display
        self.memory.chat_memory.add_ai_message(AppConfig.CHAT_INITIAL_GREETING)


    # The _convert_gradio_history_to_langchain_messages and get_feature_response
    # methods are removed as summarize and creative idea functionalities are no longer present.
    # def _convert_gradio_history_to_langchain_messages(self, gradio_history):
    #     """
    #     Converts Gradio's history (type='messages') format to LangChain's HumanMessage/AIMessage format.
    #     Used when creating temporary memories for feature-specific calls.
    #     Gradio history for type='messages' is a list of dictionaries: [{"role": "user", "content": "text"}, ...]
    #     """
    #     langchain_messages = []
    #     for msg_dict in gradio_history:
    #         if msg_dict["role"] == "user":
    #             langchain_messages.append(HumanMessage(content=msg_dict["content"]))
    #         elif msg_dict["role"] == "assistant":
    #             langchain_messages.append(AIMessage(content=msg_dict["content"]))
    #     return langchain_messages

    def get_chat_response(self, user_message: str) -> str:
        """
        Gets a response from the LLM for a general chat message.
        Automatically updates the internal conversation memory.
        """
        try:
            # Predict using the main conversation chain which manages its own memory
            ai_response = self.conversation_chain.predict(input=user_message)
            return ai_response
        except Exception as e:
            return f"Error: {e}. Please try again."

    # def get_feature_response(self, prompt_message: str, current_gradio_history: list, temperature_override: float) -> str:
    #     """
    #     Gets a response from the LLM for a specific feature (summary, creative idea).
    #     This uses a temporary chain and memory to avoid altering the main conversation flow.
    #     """
    #     try:
    #         # Create a temporary LLM instance with potentially different temperature
    #         temp_llm = ChatOpenAI(
    #             model_name=AppConfig.VLLM_MODEL_NAME,
    #             openai_api_base=AppConfig.VLLM_API_URL,
    #             openai_api_key=AppConfig.VLLM_API_KEY,
    #             temperature=temperature_override
    #         )

    #         # Create a temporary memory from the current Gradio history
    #         temp_memory = ConversationBufferMemory(return_messages=True)
    #         langchain_messages_for_temp = self._convert_gradio_history_to_langchain_messages(current_gradio_history)
    #         for msg in langchain_messages_for_temp:
    #             if isinstance(msg, HumanMessage):
    #                 temp_memory.chat_memory.add_user_message(msg.content)
    #             elif isinstance(msg, AIMessage):
    #                 temp_memory.chat_memory.add_ai_message(msg.content)

    #         temp_conversation_chain = ConversationChain(
    #             llm=temp_llm,
    #             memory=temp_memory,
    #             verbose=False
    #         )

    #         # Predict with the temporary chain
    #         response = temp_conversation_chain.predict(input=prompt_message)
    #         return response
    #     except Exception as e:
    #         return f"Error communicating with LLM for this feature: {e}"

    def get_initial_greeting(self) -> str:
        """Returns the initial greeting message for the chatbot."""
        return AppConfig.CHAT_INITIAL_GREETING

