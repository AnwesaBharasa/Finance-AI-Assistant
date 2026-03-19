from langchain_core.tools import tool

@tool
def recommend_investment(risk_profile: str, investment_duration_years: str) -> str:
    """Recommends an investment portfolio percentage allocation based on risk level ('low', 'medium', 'high') and duration."""
    risk = str(risk_profile).lower()
    investment_duration_years = int(float(investment_duration_years))
    if risk in ["low", "conservative"]:
        return (
            "Recommended Instruments: Fixed Deposits (FD), Corporate Bonds, Public Provident Fund (PPF).\n"
            "Suggested Allocation:\n"
            "- 70% Debt & Bonds (Low Risk)\n"
            "- 20% FDs / PPF (Guaranteed)\n"
            "- 10% Liquid Mutual Funds (Accessibility)"
        )
    elif risk in ["medium", "balanced", "moderate"]:
        return (
            "Recommended Instruments: Index Funds, Balanced Advantage Funds, Corporate Bonds.\n"
            "Suggested Allocation:\n"
            "- 50% Equity Mutual Funds (Index/Large Cap)\n"
            "- 40% Debt Mutual Funds / Bonds\n"
            "- 10% Gold / Liquid Assets"
        )
    elif risk in ["high", "aggressive", "very high"]:
        return (
            "Recommended Instruments: Small/Mid-Cap Mutual Funds, Direct Stocks, Sectoral Funds.\n"
            "Suggested Allocation:\n"
            "- 70% Direct Equity & Mid/Small Cap Funds\n"
            "- 20% Large/Flexi Cap Mutual Funds\n"
            "- 10% Emergency Liquid/Debt"
        )
    return "Please specify risk as 'low', 'medium', or 'high', and a valid duration."
