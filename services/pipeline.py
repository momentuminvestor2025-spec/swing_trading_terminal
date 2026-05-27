import pandas as pd
import streamlit as st
from services.data_fetcher import fetch_nifty500_tickers, fetch_historical_data
from analysis.indicators import calculate_technical_indicators, calculate_mansfield_rs
from analysis.stage_analysis import classify_weinstein_stage
from scanners.vcp_scanner import score_vcp_structure
from scanners.institutional import scan_institutional_activity
from analysis.scoring import calculate_composite_score

def run_analytics_pipeline(tickers_limit=50) -> pd.DataFrame:
    """
    Main background analytics driver. Maps indicators, evaluates scanners, 
    and applies composite multi-factor structural scoring.
    """
    all_tickers = fetch_nifty500_tickers()
    selected_tickers = all_tickers[:tickers_limit]  # Adjustable ceiling boundary limit
    
    # Load Benchmark for Relative Strength Calculations
    nifty_bench = fetch_historical_data("^NSEI")
    
    results = []
    
    progress_bar = st.progress(0)
    for idx, ticker in enumerate(selected_tickers):
        progress_bar.progress((idx + 1) / len(selected_tickers))
        df = fetch_historical_data(ticker)
        
        if df.empty or len(df) < 200:
            continue
            
        # Transform structural columns
        df = calculate_technical_indicators(df)
        df = calculate_mansfield_rs(df, nifty_bench)
        
        # Pull last processed variables
        latest = df.iloc[-1]
        
        # Evaluate Screener modules
        stage_info = classify_weinstein_stage(df)
        vcp_score = score_vcp_structure(df)
        inst_score = scan_institutional_activity(df)
        
        # Calculate Base Scores
        rsi = latest['RSI']
        momentum_score = 50.0
        if latest['Close'] > latest['EMA20'] > latest['EMA50']: momentum_score += 25
        if rsi > 60: momentum_score += 25
            
        rs_score = 50.0 + (latest['Mansfield_RS'] * 5)
        rs_score = min(max(rs_score, 10.0), 100.0)
        
        # Bundle into scoring matrix
        metrics = {
            "momentum_score": momentum_score,
            "rs_score": rs_score,
            "vcp_score": vcp_score,
            "inst_score": inst_score,
            "stage_score": stage_info['score'],
            "fundamental_score": 75.0, # Placeholder structure for dynamic API ingestion expansion
            "valuation_score": 60.0
        }
        
        score_res = calculate_composite_score(metrics)
        
        results.append({
            "Symbol": ticker.replace(".NS", ""),
            "Price": round(latest['Close'], 2),
            "RSI": round(rsi, 1),
            "Stage": stage_info['stage'],
            "VCP Score": round(vcp_score, 1),
            "Inst Score": round(inst_score, 1),
            "RS Rating": round(rs_score, 1),
            "Final Score": score_res['final_score'],
            "Setup Tier": score_res['tier']
        })
        
    progress_bar.empty()
    return pd.DataFrame(results)