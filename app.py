import streamlit as st
import pandas as pd
from database.db_manager import init_db, add_to_watchlist, remove_from_watchlist, get_watchlist
from services.pipeline import run_analytics_pipeline
from services.data_fetcher import fetch_historical_data
from analysis.indicators import calculate_technical_indicators
from charts.plotly_charts import generate_candlestick_chart

# Main Streamlit Configuration Setup
st.set_page_config(page_title="AlphaAxis Trading Terminal", layout="wide", initial_sidebar_state="expanded")

# Initialize Database Architecture
init_db()

# Application Title Layout Framework
st.title("⚡ AlphaAxis Institutional Swing Trading Terminal")
st.caption("Industrial Scale Screening Engine & Quantitative Alpha Allocator for Nifty 500")
st.markdown("---")

# Navigation Menu Bar Container
menu_selection = st.sidebar.radio("Navigation Control Panel", ["Market Matrix Engine", "Watchlist Monitor", "Deep Dive Module"])

# Global Run Automation Framework
if "processed_data" not in st.session_state:
    st.session_state["processed_data"] = None

# Sidebar Pipeline Controls
st.sidebar.header("Pipeline Controls")
ticker_limit = st.sidebar.slider("Scan Execution Ceiling Limit (Stocks)", 10, 500, 50)

if st.sidebar.button("Execute Realtime Market Scan") or st.session_state["processed_data"] is初 None:
    with st.spinner("Processing alpha factors across underlying datasets..."):
        st.session_state["processed_data"] = run_analytics_pipeline(tickers_limit=ticker_limit)

df_scanned = st.session_state["processed_data"]

# ----------------- MAIN VIEWPORTS -----------------

if menu_selection == "Market Matrix Engine":
    st.subheader("📊 Macro Terminal Screener Overview Matrix")
    
    # Global Scoring Summary Statistics
    if df_scanned is not None and not df_scanned.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Analyzed Assets Cluster", len(df_scanned))
        c2.metric("Elite / A+ Setups Discovered", len(df_scanned[df_scanned['Final Score'] >= 80]))
        c3.metric("Stage 2 Acceleration Tracks", len(df_scanned[df_scanned['Stage'].str.contains("Stage 2")]))
        c4.metric("High Volume Accumulations Found", len(df_scanned[df_scanned['Inst Score'] >= 75]))
        
        st.markdown("---")
        
        # Interactive Filtering Framework Columns
        st.markdown("### 🔍 Advanced Filter Array Matrix")
        tier_filter = st.multiselect("Filter by Setup Tier Class", options=df_scanned['Setup Tier'].unique(), default=df_scanned['Setup Tier'].unique())
        df_filtered = df_scanned[df_scanned['Setup Tier'].isin(tier_filter)]
        
        # Render Processed Interactive Data Table Core Framework
        st.dataframe(
            df_filtered.sort_values(by="Final Score", ascending=False),
            use_container_width=True,
            column_config={
                "Price": st.column_config.NumberColumn(format="₹ %.2f"),
                "Final Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f")
            }
        )
    else:
        st.info("Execute a scan to view data.")

elif menu_selection == "Watchlist Monitor":
    st.subheader("📋 Watchlist Core Matrix Monitor")
    
    wl_symbols = get_watchlist()
    
    c1, c2 = st.columns([1, 3])
    with c1:
        new_symbol = st.text_input("Append Asset To Tracking Hub (e.g. RELIANCE)").upper()
        if st.button("Commit Asset to Registry"):
            if new_symbol:
                add_to_watchlist(f"{new_symbol}.NS")
                st.success("Committed successfully!")
                st.rerun()
                
        remove_symbol = st.selectbox("Purge Target Asset Reference", options=[""] + wl_symbols)
        if st.button("Drop Target Reference") and remove_symbol != "":
            remove_from_watchlist(remove_symbol)
            st.success("Purged successfully!")
            st.rerun()
            
    with c2:
        if wl_symbols:
            st.write("### Active Tracked Elements Watchlist")
            tracking_clean = [s.replace(".NS", "") for s in wl_symbols]
            st.info(f"Currently tracking monitoring queues for: {', '.join(tracking_clean)}")
        else:
            st.warning("Watchlist repository database context is empty.")

elif menu_selection == "Deep Dive Module":
    st.subheader("🎯 Institutional Technical Verification Engine")
    
    if df_scanned is not None and not df_scanned.empty:
        target_ticker = st.selectbox("Select Core Vector Asset for Visualization Analysis", options=df_scanned['Symbol'].tolist())
        
        if target_ticker:
            with st.spinner("Compiling multi-timeframe geometric chart layout..."):
                full_ticker = f"{target_ticker}.NS"
                raw_hist = fetch_historical_data(full_ticker)
                
                if not raw_hist.empty:
                    processed_hist = calculate_technical_indicators(raw_hist)
                    fig = generate_candlestick_chart(processed_hist, target_ticker)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Highlight metadata stats
                    meta = df_scanned[df_scanned['Symbol'] == target_ticker].iloc[0]
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Composite Processing Matrix Score", meta['Final Score'])
                    col2.metric("Volatility Contraction (VCP)", meta['VCP Score'])
                    col3.metric("Institutional Volume Pressure", meta['Inst Score'])
                    col4.metric("Mansfield Relative Strength Strength", meta['RS Rating'])