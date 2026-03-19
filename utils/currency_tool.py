import yfinance as yf
from langchain_core.tools import tool

@tool
def convert_currency(amount: str, from_currency: str, to_currency: str) -> str:
    """Converts an amount from one currency to another using real-time forex rates (e.g., from 'USD' to 'INR')."""
    try:
        amount = float(amount)
        from_curr = str(from_currency).upper().strip()
        to_curr = str(to_currency).upper().strip()
        
        if from_curr == to_curr:
            return f"{amount:,.2f} {from_curr} is equal to {amount:,.2f} {to_curr} (No conversion needed)."
        
        # yfinance uses symbols like 'USDINR=X'
        symbol = f"{from_curr}{to_curr}=X"
        data = yf.Ticker(symbol)
        
        # Get the latest price
        rate = data.info.get("regularMarketPrice") or data.info.get("previousClose")
        
        if rate is None:
            # Try inverse if not found
            alt_symbol = f"{to_curr}{from_curr}=X"
            alt_data = yf.Ticker(alt_symbol)
            alt_rate = alt_data.info.get("regularMarketPrice") or alt_data.info.get("previousClose")
            if alt_rate:
                rate = 1 / alt_rate
        
        if rate is None:
            return f"Could not fetch exchange rate for {from_curr}/{to_curr}. Please check the currency codes."
            
        converted_amount = amount * rate
        
        return (
            f"Currency Conversion:\n"
            f"- Input: {amount:,.2f} {from_curr}\n"
            f"- Exchange Rate: {rate:,.4f}\n"
            f"- **Converted Amount: {converted_amount:,.2f} {to_curr}**\n"
            f"(Data provided by Yahoo Finance Forex)"
        )
    except Exception as e:
        return f"Currency conversion error: {str(e)}"
