import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.calculator import calculate_emi, calculate_sip
from utils.budget_tool import plan_budget
from utils.investment_tool import recommend_investment
from utils.tax_tool import calculate_tax_optimization
from utils.market_tool import get_stock_price
from utils.rag_logic import rag_search_tool
from utils.search_logic import get_web_search_tool

def get_document_tools():
    """Returns tools bound strictly to document knowledge and calculations."""
    return [
        calculate_emi,
        calculate_sip,
        plan_budget,
        recommend_investment,
        calculate_tax_optimization,
        get_stock_price,
        rag_search_tool()
    ]

def get_web_tools():
    """Returns tools capable of broad web search and calculations."""
    return [
        calculate_emi,
        calculate_sip,
        plan_budget,
        recommend_investment,
        calculate_tax_optimization,
        get_stock_price,
        get_web_search_tool()
    ]
