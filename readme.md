# GenAI-main Utilities

This folder contains several small automation and data tools built with Python.  
They demonstrate web scraping, browser automation, stock tracking, and a Streamlit dashboard.

## Contents

- `wiki.py` – Scrape quotes from a website into Excel (Playwright).
- `streamlit_app.py` – Streamlit dashboard for Indian stock market analysis + investment calculator.
- `stock.py` – Console-based real-time stock price tracker with alerts (US stocks).
- `seleniumn.py` – Selenium scraper for SauceDemo products into Excel.
- `demo_screen.py` – Basic desktop automation to open a Google search result.

---

## 1. `wiki.py` – Quotes Scraper (Playwright + Excel)

### What it does

- Opens `http://quotes.toscrape.com/` using Playwright.
- Collects up to the first **10 quotes** on the page (text, author, tags).
- Saves them into an Excel file named `Top_10_Quotes.xlsx`.
- Prints a small preview in the terminal.

### Key technologies

- `asyncio`
- `playwright` (Chromium)
- `pandas` (for Excel export)

### How to run

1. Install dependencies (example):

   pip install playwright pandas
   playwright install
   

Run the script:
   python wiki.py
Output:
File: Top_10_Quotes.xlsx in the current folder.
Columns: Quote, Author, Tags.


2. streamlit_app.py – NSE Pro Dashboard & Wealth Calculator
What it does
Provides a Streamlit dashboard for selected NSE (India) stocks.

Features:
Sector and stock selection from predefined lists.
Downloads historical data via Yahoo Finance (yfinance).
Computes and plots:
Candlestick chart (Open/High/Low/Close).
50-day and 200-day moving averages (DMA).
Shows key metrics:
Current price and daily change.
Period high and low.
Includes an investment calculator tab:
Monthly SIP and one-time lumpsum styles.
Calculates total invested, estimated future value, and profit.
Visualizes principal vs. profit with a pie chart.
Key technologies
streamlit
yfinance
plotly (for charts)
datetime utilities

How to run
Install dependencies (example):
   pip install streamlit yfinance plotly
From the folder containing streamlit_app.py, run:
   streamlit run streamlit_app.py

In the UI:
Use the sidebar to:
Select a sector (e.g., Banking & Finance, IT Services).
Select a stock ticker within that sector (e.g., HDFCBANK.NS).
Choose the analysis period in days (30–730).

Use the "Market Analysis" tab for charts and price metrics.

Use the "Investment Calculator" tab for SIP / lumpsum projections.

3. stock.py – Real-Time Stock Price Tracker (Console)

What it does
Monitors a fixed watchlist of US stocks:
AMZN, CSCO, ORCL, AAPL, TSLA

For each symbol:
Fetches 1-minute interval intraday data for the current day using yfinance.
Prints the latest closing price in the console.
Issues an alert if the price goes below a configured threshold.
Runs in an infinite loop with updates every 15 seconds until you press Ctrl + C.

Key technologies
yfinance
time

How to run
Install dependency:
   pip install yfinance

Run the script:
   python stock.py

Behavior:
Shows an update timestamp for each cycle.
Prints each stock’s current price.
Prints an alert line when current_price < limit for that ticker.
Stop with Ctrl + C.

Customization:
Edit the watchlist dictionary in the script to:
Add/remove tickers.
Change alert price levels.

4. seleniumn.py – SauceDemo Product Scraper (Selenium + Excel)

What it does
Launches Chrome via Selenium.
Opens https://www.saucedemo.com/.
Logs in using demo credentials:
Username: standard_user
Password: secret_sauce
Waits for products to load.

Scrapes each product’s:
Name
Price
Saves the data to SauceDemo_Products.xlsx.
Key technologies
selenium (WebDriver, waits, locators)
pandas (for Excel export)

Prerequisites
Google Chrome installed.
ChromeDriver compatible with your Chrome version, available on PATH,
or managed by a driver manager if you integrate one.

How to run
Install dependencies:
   pip install selenium pandas
Ensure ChromeDriver is set up.
Run the script:
   python seleniumn.py

Output:
File: SauceDemo_Products.xlsx in the current folder.
Columns: Product, Price.
Notes:
To run Chrome in headless mode, uncomment the chrome_options.add_argument("--headless") line in the script.
	
5. demo_screen.py – Simple Google Search Click Automation
What it does
Builds a Google search URL for:
  india vs newzealand T20 schedule
Opens the search in your default browser.
Waits 10 seconds for the page to load.
Uses pyautogui to click at a fixed screen coordinate (approx. where the first Google result usually appears).
Key technologies
pyautogui
webbrowser
time

How to run
Install dependency:
   pip install pyautogui

Run the script:
   python demo_screen.py
Important notes / safety
pyautogui.click(400, 450) uses absolute screen coordinates:
This may need adjustment based on your screen resolution, scaling, and browser layout.
If the click misses the intended link, move your mouse to the desired area, use pyautogui.position() in a Python shell to find better coordinates, and update the script.
There is no error handling if the page loads slowly; increase time.sleep(10) if needed.
General Setup
Recommended Python version
Python 3.8+.
Virtual environment (optional but recommended)
python -m venv .venv.\.venv\Scripts\activate  # On Windowspip install --upgrade pip
Then install the libraries each script needs (or create a shared requirements.txt).