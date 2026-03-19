from langchain_core.tools import tool

@tool
def calculate_emi(principal: str, annual_interest_rate: str, tenure_years: str) -> str:
    """Calculates the Equated Monthly Installment (EMI) for a loan given the principal, annual interest rate, and tenure in years."""
    try:
        principal = float(principal)
        annual_interest_rate = float(annual_interest_rate)
        tenure_years = int(float(tenure_years))
        r = (annual_interest_rate / 12) / 100
        n = tenure_years * 12
        if r == 0:
            emi = principal / n
        else:
            emi = principal * r * ((1 + r)**n) / (((1 + r)**n) - 1)
        total_payment = emi * n
        interest_payable = total_payment - principal
        return f"Monthly EMI: Rs.{emi:,.2f} | Total Interest: Rs.{interest_payable:,.2f} | Total Payment: Rs.{total_payment:,.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

@tool
def calculate_sip(monthly_investment: str, expected_annual_return: str, years: str) -> str:
    """Calculates the estimated returns for a Systematic Investment Plan (SIP)."""
    try:
        monthly_investment = float(monthly_investment)
        expected_annual_return = float(expected_annual_return)
        years = int(float(years))
        n = years * 12
        i = (expected_annual_return / 100) / 12
        future_value = monthly_investment * (((1 + i)**n - 1) / i) * (1 + i)
        total_invested = monthly_investment * n
        estimated_return = future_value - total_invested
        return f"Total Invested: Rs.{total_invested:,.2f} | Est. Returns: Rs.{estimated_return:,.2f} | Total Value: Rs.{future_value:,.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"
