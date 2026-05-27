import pandas as pd
from config.settings import *

def calculate_composite_score(metrics: dict) -> dict:
    """
    Combines core structural and qualitative filters into a single dynamic factor rank.
    """
    # Safeguard missing fundamentals gracefully
    f_score = metrics.get('fundamental_score', 60.0)
    v_score = metrics.get('valuation_score', 50.0)
    
    weighted_total = (
        f_score * WEIGHT_EARNINGS +
        metrics['momentum_score'] * WEIGHT_MOMENTUM +
        metrics['rs_score'] * WEIGHT_RS +
        metrics['vcp_score'] * WEIGHT_VCP +
        metrics['inst_score'] * WEIGHT_INSTITUTIONAL +
        metrics['stage_score'] * WEIGHT_STAGE +
        v_score * WEIGHT_VALUATION
    )
    
    # Tier allocation
    if weighted_total >= 90:
        tier = "Elite Setup"
    elif weighted_total >= 80:
        tier = "A+ Setup"
    elif weighted_total >= 70:
        tier = "Strong Setup"
    elif weighted_total >= 60:
        tier = "Watchlist Tier"
    else:
        tier = "Avoid / Out of Favor"
        
    return {
        "final_score": round(weighted_total, 2),
        "tier": tier
    }