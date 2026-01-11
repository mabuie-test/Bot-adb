"""
storage.py
Utilitários para extrair batches do SQLite e export para Parquet/Pandas.
"""
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join('data', 'data.db')

def fetch_ticks(limit=10000):
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('SELECT * FROM ticks ORDER BY id DESC LIMIT ?', conn, params=(limit,))
    conn.close()
    return df

def export_parquet(path='data/ticks.parquet'):
    df = fetch_ticks(limit=1000000)
    df.to_parquet(path, index=False)
    return path

