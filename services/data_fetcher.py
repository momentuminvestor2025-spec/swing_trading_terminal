import pandas as pd
import yfinance as yf
import streamlit as st
import requests
from config.settings import NIFTY_500_URL

@st.cache_data(ttl=86400)  # Cache for 24 hours
def fetch_nifty500_tickers():
    """Dynamically parses and cleans up the live Nifty 500 catalog straight from the NSE source."""
    try:
        df = pd.read_csv(NIFTY_500_URL)
        # Append standard NSE structural ticker format for yfinance mapping
        tickers = [f"{sym}.NS" for sym in df['Symbol'].strip().tolist()]
        return tickers
    except Exception:
        # High reliability structural failover fallback list
        return ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "ITC.NS"]

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def fetch_historical_data(ticker: str, period="2y") -> pd.DataFrame:
    """Retrieves standard timeframe history for underlying tracking."""
    try:
        obj = yf.Ticker(ticker)
        df = obj.history(period=period)
        if df.empty:
            return pd.DataFrame()
        return df
    except Exception:
        return pd.DataFrame()