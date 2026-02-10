import yfinance as yf
import time

def track_stocks():
    # Updated watchlist with Amazon, Cisco, and Oracle
    watchlist = {
        "AMZN": 180.00,  # Amazon
        "CSCO": 45.00,   # Cisco
        "ORCL": 160.00,  # Oracle
        "AAPL": 150.00,  # Apple
        "TSLA": 180.00   # Tesla
    }

    print("--- Extended Stock Tracker Starting ---")
    print("Monitoring: " + ", ".join(watchlist.keys()))
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            print(f"Update Time: {time.strftime('%H:%M:%S')}")
            print("-" * 35)

            for ticker, limit in watchlist.items():
                stock = yf.Ticker(ticker)
                # Fetching 1-minute interval data for the current day
                data = stock.history(period="1d", interval="1m")
                
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    print(f"{ticker:5}: ${current_price:>8.2f}")

                    if current_price < limit:
                        print(f"  ⚠️ ALERT: {ticker} is below ${limit}!")
                else:
                    print(f"Error fetching {ticker}")

            print("-" * 35)
            time.sleep(15) # Checking every 15 seconds

    except KeyboardInterrupt:
        print("\nTracker stopped.")

if __name__ == "__main__":
    track_stocks()