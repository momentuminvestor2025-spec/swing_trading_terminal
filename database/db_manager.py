import sqlite3
import pandas as pd
import os
from config.settings import DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Watchlist Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            symbol TEXT PRIMARY KEY,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cache / Historical Ranking Table for Performance Tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical_rankings (
            date TEXT,
            symbol TEXT,
            score REAL,
            rank INTEGER,
            PRIMARY KEY (date, symbol)
        )
    ''')
    conn.commit()
    conn.close()

def add_to_watchlist(symbol: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO watchlist (symbol) VALUES (?)", (symbol,))
        conn.commit()
    finally:
        conn.close()

def remove_from_watchlist(symbol: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM watchlist WHERE symbol = ?", (symbol,))
        conn.commit()
    finally:
        conn.close()

def get_watchlist():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT symbol FROM watchlist", conn)
        return df['symbol'].tolist()
    finally:
        conn.close()