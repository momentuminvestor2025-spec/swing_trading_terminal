import pandas as pd
import numpy as np

def score_vcp_structure(df: pd.DataFrame) -> float:
    """
    Evaluates Volatility Contraction Characteristics (Mark Minervini Rules).
    Checks rolling standard deviation compression and ATR contraction alongside volume dry-up.
    """
    if len(df) < 60:
        return 50.0
    
    # 1. Volatility Compression Check
    recent_atr_pct = df['Roll_ATR_Pct'].iloc[-1]
    prior_atr_pct = df['Roll_ATR_Pct'].iloc[-30:-10].mean()
    
    atr_compress_ratio = prior_atr_pct / recent_atr_pct if recent_atr_pct > 0 else 1
    
    # 2. Volume Dry-Up Check (VUD) on tight ranges
    recent_vol_sma = df['Volume'].iloc[-5:].mean()
    base_vol_sma = df['Volume'].iloc[-30:-5].mean()
    vol_dryup_ratio = base_vol_sma / recent_vol_sma if recent_vol_sma > 0 else 1
    
    # Score Calculation
    vcp_score = 50.0
    if atr_compress_ratio > 1.2:  # Volatility has shrunk by > 20%
        vcp_score += 25
    if vol_dryup_ratio > 1.3:    # Volume has dried up significantly
        vcp_score += 25
        
    # Boundary capping
    return min(max(vcp_score, 10.0), 100.0)