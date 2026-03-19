import os
import sys
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import Config
from utils.search_logic import get_web_search_tool

def get_chatgroq_model():
    """Initialize and return the LangChain Tool-Calling Agent"""
    try:
        # Initialize the Groq chat model
        llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.MODEL_NAME,
            temperature=0,
        )
        
        # Get Tools
        tools = [get_web_search_tool()]
        
        # Define Prompt Template for Tool Calling Agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a STRICT AI Agri-Consultant Chatbot. Your ONLY domain is agriculture, crop diseases, farming, weather, and agricultural market prices. If a user asks a question that is NOT strictly related to these agricultural domains, you MUST politely refuse to answer and state that you are an AI Agri-Consultant and can only answer questions related to agriculture and farming.\n\nFor agricultural queries: Respond to the user's queries regarding crop diseases and farming. You must prefer providing advice from the uploaded document (RAG). Use the web search tool if you need live weather or market prices, or if no document context is retrieved. Provide practical, farmer-friendly advice. Diagnose crop diseases from symptoms, suggest remedies and prevention.\n\nAlways cite your source clearly as 'From uploaded document', 'From web search', or 'From my knowledge'. Avoid hallucination: Say 'I don't have enough information' if unsure.\n\nRAG Context (if any): {context}\n\nSystem Prompt / Instructions: {system_prompt}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create Tool Calling Agent
        agent = create_tool_calling_agent(llm, tools, prompt)
        
        # Initialize Memory
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="input")
        
        # Create Agent Executor
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            memory=memory, 
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent_executor
        
    except Exception as e:
        raise RuntimeError(f"Failed to initialize agent: {str(e)}")