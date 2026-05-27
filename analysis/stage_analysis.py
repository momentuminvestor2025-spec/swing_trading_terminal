import pandas as pd

def classify_weinstein_stage(df: pd.DataFrame) -> dict:
    """
    Classifies a stock into one of Stan Weinstein's 4 Market Stages:
    Stage 1: Accumulation | Stage 2: Uptrend | Stage 3: Distribution | Stage 4: Downtrend
    """
    if len(df) < 200 or 'EMA200' not in df.columns:
        return {"stage": "Unknown", "score": 50, "desc": "Insufficient data"}
    
    row = df.iloc[-1]
    prev_row = df.iloc[-20] # Check trend over ~1 month
    
    price = row['Close']
    ema200 = row['EMA200']
    ema50 = row['EMA50']
    
    # Check slope of EMA200
    ema200_flat = abs(ema200 - prev_row['EMA200']) / prev_row['EMA200'] < 0.02
    ema200_rising = ema200 > prev_row['EMA200'] and not ema200_flat
    ema200_falling = ema200 < prev_row['EMA200'] and not ema200_flat
    
    if price > ema200 and ema200_rising and ema50 > ema200:
        return {"stage": "Stage 2 (Uptrend)", "score": 100, "desc": "Strong Institutional Markup"}
    elif price < ema200 and ema200_falling and ema50 < ema200:
        return {"stage": "Stage 4 (Downtrend)", "score": 10, "desc": "Capitulation / Liquidation"}
    elif price > ema200 and ema200_flat:
        return {"stage": "Stage 1 (Accumulation)", "score": 60, "desc": "Base Formation/Early Breakout Candidate"}
    else:
        return {"stage": "Stage 3 (Distribution)", "score": 30, "desc": "Institutional Churn / Top Building"}