import os
import sys
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.router import get_document_tools, get_web_tools
from utils.memory import get_memory
from models.llm import get_chatgroq_model

def get_finance_agent_executor(mode: str = "Document Search", response_style: str = "Detailed"):
    """Initializes and returns the tool-calling agent executor based on the selected mode."""
    try:
        llm = get_chatgroq_model()
        
        style_prompt = f"You must keep your answers STRICTLY {response_style}. If Concise, be extremely brief. If Detailed, step-by-step elaborations with full context.\nCRITICAL RULE: Once you receive the output of a tool, synthesize your final response and STOP. Do NOT call the same tool again, and DO NOT call other tools unless strictly necessary."
        
        if mode == "Document Search":
            tools = get_document_tools()
            system_prompt = f"""You are a STRICT Finance and Tax AI Assistant.
Your ONLY source of domain knowledge is the uploaded document provided via the document_search tool.
You may use the calculators for math.
If the user asks a question that requires external knowledge, or if the document_search tool returns 'This is outside my document knowledge.', you MUST literally reply 'This is outside my document knowledge.' and politely refuse to answer. Do not use your own internal knowledge.
{style_prompt}"""
        else:
            tools = get_web_tools()
            system_prompt = f"""You are a helpful AI Assistant with web search capabilities.
You have access to a web search tool and calculation tools.
You can answer ANY question the user asks, including questions entirely unrelated to finance.
If you don't know the answer, use the web search tool to find it. You must answer questions from any domain.
{style_prompt}"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(llm, tools, prompt)
        memory = get_memory()
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        return agent_executor
    except Exception as e:
        raise RuntimeError(f"Failed to initialize agent: {str(e)}")
