from langchain_core.tools import tool

@tool
def calculate_fd(principal: str, annual_rate: str, years: str, compounding_frequency: str = "quarterly") -> str:
    """Calculates Fixed Deposit (FD) maturity amount. Compounding frequency can be 'monthly', 'quarterly', 'half-yearly', or 'yearly'."""
    try:
        P = float(principal)
        r = float(annual_rate) / 100
        t = float(years)
        
        freq_map = {
            "monthly": 12,
            "quarterly": 4,
            "half-yearly": 2,
            "yearly": 1
        }
        n = freq_map.get(compounding_frequency.lower(), 4)
        
        # Formula: A = P(1 + r/n)^(n*t)
        maturity_amount = P * (1 + r/n)**(n*t)
        total_interest = maturity_amount - P
        
        return (
            f"FD Maturity Details:\n"
            f"- Principal: Rs.{P:,.2f}\n"
            f"- Interest Rate: {annual_rate}%\n"
            f"- Tenure: {years} years\n"
            f"- Compounding: {compounding_frequency.capitalize()}\n"
            f"- Total Interest Earned: Rs.{total_interest:,.2f}\n"
            f"- **Maturity Amount: Rs.{maturity_amount:,.2f}**"
        )
    except Exception as e:
        return f"FD Calculation error: {str(e)}"
