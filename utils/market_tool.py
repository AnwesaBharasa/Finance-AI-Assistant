import yfinance as yf
from langchain_core.tools import tool

@tool
def get_stock_price(ticker_symbol: str) -> str:
    """Fetches live stock/index price, 52-week range, and key metrics for a given ticker symbol. Use '^NSEI' for Nifty 50, '^BSESN' for Sensex, or company tickers like 'RELIANCE.NS', 'TCS.NS', 'INFY.NS'."""
    try:
        ticker_symbol = str(ticker_symbol).strip().upper()
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        name = info.get("shortName", ticker_symbol)
        price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
        currency = info.get("currency", "INR")
        day_high = info.get("dayHigh", "N/A")
        day_low = info.get("dayLow", "N/A")
        week_52_high = info.get("fiftyTwoWeekHigh", "N/A")
        week_52_low = info.get("fiftyTwoWeekLow", "N/A")
        market_cap = info.get("marketCap")
        pe_ratio = info.get("trailingPE", "N/A")

        if price is None:
            return f"Could not fetch price for '{ticker_symbol}'. Please verify the ticker symbol (e.g., 'RELIANCE.NS' for NSE stocks, '^NSEI' for Nifty 50)."

        # Format market cap
        if market_cap:
            if market_cap >= 1e12:
                mc_str = f"{market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                mc_str = f"{market_cap/1e9:.2f}B"
            elif market_cap >= 1e7:
                mc_str = f"{market_cap/1e7:.2f}Cr"
            else:
                mc_str = f"{market_cap:,.0f}"
        else:
            mc_str = "N/A"

        return (
            f"Live Market Data for {name} ({ticker_symbol}):\n"
            f"- Current Price: {currency} {price:,.2f}\n"
            f"- Day Range: {day_low} - {day_high}\n"
            f"- 52-Week Range: {week_52_low} - {week_52_high}\n"
            f"- Market Cap: {mc_str}\n"
            f"- P/E Ratio: {pe_ratio}"
        )
    except Exception as e:
        return f"Error fetching market data: {str(e)}"
