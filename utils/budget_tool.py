from langchain_core.tools import tool

@tool
def plan_budget(monthly_income: str, fixed_expenses: str = "0", savings_goal: str = "0") -> str:
    """Calculates a recommended budget allocation based on the 50/30/20 rule, factoring in fixed expenses and goals."""
    try:
        monthly_income = float(monthly_income)
        fixed_expenses = float(fixed_expenses)
        savings_goal = float(savings_goal)
        needs = monthly_income * 0.50
        wants = monthly_income * 0.30
        savings = monthly_income * 0.20
        
        plan = (
            f"Structured Budget Plan for Income: Rs.{monthly_income:,.2f}\n\n"
            f"Recommended Target Allocation:\n"
            f"- Needs (50% rule): Spend up to Rs.{needs:,.2f} (Your fixed expenses: Rs.{fixed_expenses:,.2f})\n"
            f"- Wants (30% rule): Spend up to Rs.{wants:,.2f}\n"
            f"- Savings (20% rule): Save strictly Rs.{savings:,.2f} (Your savings goal: Rs.{savings_goal:,.2f})"
        )
        return plan
    except Exception as e:
        return f"Budget error: {str(e)}"
