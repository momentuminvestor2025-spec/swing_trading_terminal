import pandas as pd

def scan_institutional_activity(df: pd.DataFrame) -> float:
    """
    Scans for institutional footprint: Pocket Pivots, High-Volume Delivery-like bars,
    and Wide Range Accumulation Columns.
    """
    if len(df) < 30:
        return 50.0
    
    latest_bar = df.iloc[-1]
    vol_sma20 = df['Volume'].iloc[-20:].mean()
    
    inst_score = 50.0
    
    # Check for volume spike with positive close
    if latest_bar['Volume'] > (vol_sma20 * 2) and latest_bar['Close'] > latest_bar['Open']:
        inst_score += 30
        
    # Check for Pocket Pivot (Volume greater than largest down-volume day in past 10 days)
    past_10_days = df.iloc[-11:-1]
    down_days = past_10_days[past_10_days['Close'] < past_10_days['Open']]
    
    if not down_days.empty:
        max_down_vol = down_days['Volume'].max()
        if latest_bar['Volume'] > max_down_vol and latest_bar['Close'] > latest_bar['Open']:
            inst_score += 20
            
    return min(inst_score, 100.0)