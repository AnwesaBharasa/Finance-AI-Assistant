import os
import sys
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import Config

class WebSearchInput(BaseModel):
    query: str = Field(description="The specific search query to look up on the web (e.g., 'latest RBI repo rate', 'current Nifty 50 price').")

def web_search(query: str) -> str:
    """Search the web for financial news, market prices, and rates and return summarized results."""
    try:
        tavily_tool = TavilySearchResults(
            max_results=3,
            tavily_api_key=Config.TAVILY_API_KEY
        )
        results = tavily_tool.invoke({"query": query})
        
        if isinstance(results, list):
            summary = "\n".join([f"- {res.get('content', '')}" for res in results])
            return summary
        return str(results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

def get_web_search_tool():
    """Create and return a LangChain Tool for web search"""
    return StructuredTool.from_function(
        func=web_search,
        name="web_search",
        description="Search the web for live financial information, tax updates, or market prices.",
        args_schema=WebSearchInput
    )
    
