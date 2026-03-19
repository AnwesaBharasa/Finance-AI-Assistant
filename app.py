import streamlit as st
import os
import sys
import tempfile
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.llm import get_chatgroq_model
from utils.rag_logic import process_and_store_pdf, retrieve_context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_chat_response(agent_executor, query, system_prompt, context):
    """Get response from the tool-calling agent"""
    try:
        # Pass the current parameters to the agent executor. Memory is maintained internally by the agent.
        response = agent_executor.invoke({
            "input": query,
            "system_prompt": system_prompt,
            "context": context
        })
        return response.get("output", str(response))
    except Exception as e:
        error_msg = f"Error getting response: {str(e)}"
        logger.error(error_msg)
        return error_msg

def instructions_page():
    """Instructions and setup page"""
    st.title("The Chatbot Blueprint")
    st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")
    
    st.markdown("""
    ## 🔧 Setup
    
    This AI Agri-Consultant Chatbot requires configuration in `config/config.py` using `.env`.
    Ensure you have `GROQ_API_KEY` and `TAVILY_API_KEY` configured.
    
    ## How to Use
    1. **Go to the Chat page** (use the navigation in the sidebar).
    2. **Upload a Crop Manual** (PDF) in the sidebar. Wait for it to be processed into the knowledge base (RAG).
    3. **Select Response Mode**: Choose between Concise and Detailed.
    4. **Ask Questions**: Ask about crop diseases, or ask for live weather and market prices!
    
    ## Tips
    - The chatbot prefers information from your uploaded PDFs.
    - If it cannot find the answer in the document, it will automatically search the web.
    - Ask live queries like "What is the weather in California today?" to trigger the web search tool!
    """)

def chat_page():
    """Main chat interface page"""
    st.title("🌱 AI Agri-Consultant Chatbot")
    
    # Initialize response mode if not preset via sidebar yet
    if "response_mode" not in st.session_state:
        st.session_state.response_mode = "Detailed"

    # Define system prompt modifier based on response mode
    system_prompt = f"You are a helpful AI Agri-Consultant. Your responses must be {st.session_state.response_mode.lower()} and actionable."
    
    # Initialize Agent
    if "agent" not in st.session_state:
        try:
            with st.spinner("Initializing Agent..."):
                st.session_state.agent = get_chatgroq_model()
        except Exception as e:
            st.error(f"Failed to initialize Agent: {str(e)}")
            st.session_state.agent = None

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about crop diseases, remedies, or weather..."):
        if not prompt.strip():
            st.warning("Please enter a valid query.")
            return

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            if st.session_state.agent:
                with st.spinner("Retrieving knowledge base and analyzing query..."):
                    # 1. RAG Context Retrieval Priority
                    context = retrieve_context(prompt)
                    
                    if context:
                        logger.info("Found relevant context from RAG.")
                    else:
                        logger.info("No RAG context found. Agent may fall back to Web Search or innate knowledge.")
                    
                    # 2. Get Response (Agent will independently use web search tool if needed)
                    response = get_chat_response(st.session_state.agent, prompt, system_prompt, context)
            else:
                response = "Agent is not initialized. Please check API keys in `config/config.py`."
            
            st.markdown(response)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(
        page_title="AI Agri-Consultant",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    with st.sidebar:
        st.title("Navigation & Settings")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions"],
            index=0
        )
        
        if page == "Chat":
            st.divider()
            st.subheader("⚙️ Settings")
            st.session_state.response_mode = st.radio(
                "Response Mode:",
                ["Concise", "Detailed"],
                index=1
            )
            
            st.divider()
            st.subheader("📚 Knowledge Base")
            uploaded_file = st.file_uploader("Upload Crop Manual (PDF)", type=["pdf"])
            
            if uploaded_file is not None:
                with st.spinner("Processing Document..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        success, msg = process_and_store_pdf(tmp_path)
                        os.unlink(tmp_path)
                        
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                    except Exception as e:
                        logger.error(f"Error handling file upload: {e}")
                        st.error("Failed to process uploaded file.")
                        
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                if "agent" in st.session_state and st.session_state.agent:
                    st.session_state.agent.memory.clear()
                st.rerun()
    
    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    elif page == "Chat":
        chat_page()

if __name__ == "__main__":
    main()