# llm_service.py - LLM Interaction Service

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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
        
        # Create a prompt template that includes message history
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Respond to the user's questions and engage in conversation."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        # Create a chain with the LLM and prompt
        self.chain = self.prompt | self.llm
        
        # Initialize in-memory chat history
        self.store = {}
        self.session_id = "default_session"
        
        # Create the runnable with message history
        self.conversation_chain = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        # Initialize with the initial greeting
        self.get_session_history(self.session_id).add_ai_message(AppConfig.CHAT_INITIAL_GREETING)

    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """
        Get or create a chat history for a given session ID.
        """
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def get_chat_response(self, user_message: str) -> str:
        """
        Gets a response from the LLM for a general chat message.
        Automatically updates the internal conversation memory.
        """
        try:
            # Invoke the conversation chain with message history
            response = self.conversation_chain.invoke(
                {"input": user_message},
                config={"configurable": {"session_id": self.session_id}}
            )
            return response.content
        except Exception as e:
            return f"Error: {e}. Please try again."

    def get_initial_greeting(self) -> str:
        """Returns the initial greeting message for the chatbot."""
        return AppConfig.CHAT_INITIAL_GREETING

