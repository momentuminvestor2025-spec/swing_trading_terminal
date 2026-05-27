import os

# Application Settings
APP_NAME = "AlphaAxis Terminal"
THEME_COLOR = "#0E1117"  # Dark Theme Match

# Scoring Engine Weights (Must sum to 1.0)
WEIGHT_EARNINGS = 0.20
WEIGHT_MOMENTUM = 0.20
WEIGHT_RS = 0.20
WEIGHT_VCP = 0.15
WEIGHT_INSTITUTIONAL = 0.10
WEIGHT_STAGE = 0.10
WEIGHT_VALUATION = 0.05

# Database Config
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "terminal.db")

# Default Nifty 500 Ticker Fallback Link
NIFTY_500_URL = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"