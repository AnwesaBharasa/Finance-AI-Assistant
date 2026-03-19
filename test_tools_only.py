"""
Standalone tool test - NO LLM NEEDED.
This proves each tool executes pure Python math/logic.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.calculator import calculate_emi, calculate_sip
from utils.budget_tool import plan_budget
from utils.investment_tool import recommend_investment
from utils.tax_tool import calculate_tax_optimization

print("=" * 60)
print("TEST 1: EMI Calculator")
print("=" * 60)
result = calculate_emi.invoke({"principal": 500000, "annual_interest_rate": 8.5, "tenure_years": 10})
print(result)

print("\n" + "=" * 60)
print("TEST 2: SIP Calculator")
print("=" * 60)
result = calculate_sip.invoke({"monthly_investment": 5000, "expected_annual_return": 12, "years": 10})
print(result)

print("\n" + "=" * 60)
print("TEST 3: Budget Planner")
print("=" * 60)
result = plan_budget.invoke({"monthly_income": 100000, "fixed_expenses": 35000, "savings_goal": 25000})
print(result)

print("\n" + "=" * 60)
print("TEST 4: Investment Recommendation")
print("=" * 60)
result = recommend_investment.invoke({"risk_profile": "medium", "investment_duration_years": 10})
print(result)

print("\n" + "=" * 60)
print("TEST 5: Tax Optimization")
print("=" * 60)
result = calculate_tax_optimization.invoke({"annual_income": 1500000, "deductions": 150000})
print(result)

print("\n" + "=" * 60)
print("ALL 5 TOOLS EXECUTED SUCCESSFULLY WITH PURE PYTHON LOGIC!")
print("=" * 60)
