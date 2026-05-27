import pandas as pd
import numpy as np
import pandas_ta as ta

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Computes all technical metrics needed for institutional sorting."""
    if len(df) < 200:
        return df
    
    # EMAs
    df['EMA20'] = ta.ema(df['Close'], length=20)
    df['EMA50'] = ta.ema(df['Close'], length=50)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    
    # RSI & MACD
    df['RSI'] = ta.rsi(df['Close'], length=14)
    macd_df = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    if macd_df is not None:
        df['MACD'] = macd_df.iloc[:, 0]
        df['MACD_Signal'] = macd_df.iloc[:, 1]
        df['MACD_Hist'] = macd_df.iloc[:, 2]
    else:
        df['MACD'] = df['MACD_Signal'] = df['MACD_Hist'] = 0

    # ATR & Bollinger Bands
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
    bbands = ta.bbands(df['Close'], length=20, std=2)
    if bbands is not None:
        df['BB_Upper'] = bbands.iloc[:, 2]
        df['BB_Lower'] = bbands.iloc[:, 0]
    else:
        df['BB_Upper'] = df['BB_Lower'] = df['Close']
        
    # Volatility Check for VCP
    df['Roll_ATR_Pct'] = (df['ATR'] / df['Close']) * 100
    
    return df

def calculate_mansfield_rs(df: pd.DataFrame, benchmark_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates Mansfield Relative Strength index against Nifty 50."""
    merged = df[['Close']].merge(benchmark_df[['Close']], left_index=True, right_index=True, suffixes=('', '_bench'))
    
    # Base Ratio
    merged['Ratio'] = merged['Close'] / merged['Close_bench']
    # 52-Week (252 bars) SMA of Ratio
    merged['Ratio_SMA'] = merged['Ratio'].rolling(window=252, min_periods=50).mean()
    
    # Mansfield formula
    merged['Mansfield_RS'] = ((merged['Ratio'] / merged['Ratio_SMA']) - 1) * 10
    df['Mansfield_RS'] = merged['Mansfield_RS'].fillna(0)
    return df