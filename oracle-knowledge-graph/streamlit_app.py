import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PAGE SETUP ---
st.set_page_config(page_title="NSE Pro Dashboard", layout="wide", page_icon="🇮🇳")

# --- DATA LOADING ENGINE ---
@st.cache_data(ttl=3600)
def load_data(ticker, period_days):
    try:
        # Fetch extra data for Moving Average calculations
        start = datetime.now() - timedelta(days=period_days + 200)
        end = datetime.now()
        # CRITICAL FIX: multi_level_index=False flattens columns for Plotly compatibility
        data = yf.download(ticker, start=start, end=end, multi_level_index=False)
        return data
    except Exception as e:
        return None

# --- SECTOR DATA ---
sectors = {
    "Banking & Finance": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS", "BAJFINANCE.NS"],
    "IT Services": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", "LTIM.NS"],
    "Energy & Steel": ["RELIANCE.NS", "ADANIENT.NS", "TATASTEEL.NS", "JSWSTEEL.NS", "ONGC.NS", "COALINDIA.NS"],
    "Automobile": ["TATAMOTORS.NS", "M&M.NS", "MARUTI.NS", "EICHERMOT.NS", "BAJAJ-AUTO.NS"],
    "FMCG & Consumer": ["HINDUNILVR.NS", "ITC.NS", "ASIANPAINT.NS", "TITAN.NS", "NESTLEIND.NS", "ZOMATO.NS", "JIOFIN.NS"]
}

# --- SIDEBAR CONTROLS ---
st.sidebar.header("📊 Market Controls")
sel_sector = st.sidebar.selectbox("Select Sector", list(sectors.keys()))
sel_ticker = st.sidebar.selectbox("Select Stock", sectors[sel_sector])
timeframe = st.sidebar.slider("Analysis Period (Days)", 30, 730, 180)

# Load the data
df = load_data(sel_ticker, timeframe)

# --- MAIN INTERFACE TABS ---
tab_market, tab_calc = st.tabs(["📈 Market Analysis", "🧮 Investment Calculator"])

# --- TAB 1: MARKET ANALYSIS ---
with tab_market:
    if df is not None and not df.empty:
        # Technical Calculations
        df['MA50'] = df['Close'].rolling(50).mean()
        df['MA200'] = df['Close'].rolling(200).mean()
        plot_df = df.tail(timeframe)

        # 1. Header Metrics
        curr = plot_df['Close'].iloc[-1]
        prev = plot_df['Close'].iloc[-2]
        change = curr - prev
        
        st.title(f"Market Analysis: {sel_ticker}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Price", f"₹{curr:,.2f}", f"{change:,.2f}")
        m2.metric("Period High", f"₹{plot_df['High'].max():,.2f}")
        m3.metric("Period Low", f"₹{plot_df['Low'].min():,.2f}")

        # 2. Plotly Candlestick Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=plot_df.index, open=plot_df['Open'], high=plot_df['High'],
            low=plot_df['Low'], close=plot_df['Close'], name="Price"
        ))
        fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['MA50'], line=dict(color='orange', width=1.5), name="50 DMA"))
        fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['MA200'], line=dict(color='cyan', width=1.5), name="200 DMA"))

        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=550)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ Unable to fetch data. Check your connection or ticker.")

# --- TAB 2: INVESTMENT CALCULATOR ---
with tab_calc:
    st.title("🧮 Wealth Growth Calculator")
    
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        st.subheader("Configuration")
        calc_type = st.radio("Style", ["Monthly SIP", "One-time Lumpsum"])
        inv_amt = st.number_input("Investment Amount (₹)", min_value=500, value=10000, step=500)
        exp_ret = st.slider("Expected Annual Return (%)", 5, 25, 12)
        years = st.slider("Tenure (Years)", 1, 30, 10)

        # Calculation Logic
        n = years * 12
        r = exp_ret / 100 / 12
        if calc_type == "Monthly SIP":
            total_inv = inv_amt * n
            f_val = inv_amt * (((1 + r)**n - 1) / r) * (1 + r)
        else:
            total_inv = inv_amt
            f_val = inv_amt * (1 + (exp_ret/100))**years
        
        profit = f_val - total_inv

    with col_out:
        st.subheader("Returns Breakdown")
        st.write(f"Total Invested: **₹{total_inv:,.0f}**")
        st.success(f"Estimated Future Value: **₹{f_val:,.0f}**")
        
        # Pie Chart for Wealth Distribution
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Principal Invested', 'Wealth Gained'],
            values=[total_inv, profit],
            hole=.5,
            marker=dict(colors=['#1f77b4', '#00cc96'])
        )])
        fig_pie.update_layout(template="plotly_dark", height=400, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)