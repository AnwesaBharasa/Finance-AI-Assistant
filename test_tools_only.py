# Standalone Test for Phase 3 & 4 Financial Tools
# Run with: python test_tools_only.py

from utils.calculator import calculate_emi, calculate_sip
from utils.budget_tool import plan_budget
from utils.investment_tool import recommend_investment
from utils.tax_tool import calculate_tax_optimization
from utils.market_tool import get_stock_price
from utils.calculator_fd import calculate_fd
from utils.currency_tool import convert_currency

def test_tools():
    print("--- Phase 3 & 4 Tool Logic Test ---")
    
    # 1. EMI Test
    print("\n1. EMI Test (5L loan, 8.5%, 10yr):")
    print(calculate_emi.invoke({"principal": "500000", "annual_interest_rate": "8.5", "tenure_years": "10"}))
    
    # 2. Budget Test
    print("\n2. Budget Test (1L income, 35k fixed, 20k goal):")
    print(plan_budget.invoke({"monthly_income": "100000", "fixed_expenses": "35000", "savings_goal": "20000"}))
    
    # 3. Tax Test
    print("\n3. Tax Test (15L income, 1.5L deductions):")
    print(calculate_tax_optimization.invoke({"annual_income": "1500000", "deductions": "150000"}))
    
    # 4. Investment Test
    print("\n4. Investment Test (High risk, 15yr):")
    print(recommend_investment.invoke({"risk_profile": "high", "investment_duration_years": "15"}))
    
    # 5. Market Test (Verify yfinance is working for Nifty)
    print("\n5. Market Test (Live Nifty 50):")
    print(get_stock_price.invoke({"ticker_symbol": "^NSEI"}))
    
    # 6. FD Test
    print("\n6. FD Test (1L principal, 7%, 5yr, Monthly):")
    print(calculate_fd.invoke({"principal": "100000", "annual_rate": "7", "years": "5", "compounding_frequency": "monthly"}))
    
    # 7. Currency Test
    print("\n7. Currency Conversion Test (100 USD to INR):")
    print(convert_currency.invoke({"amount": "100", "from_currency": "USD", "to_currency": "INR"}))

if __name__ == "__main__":
    test_tools()
