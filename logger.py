"""
logger.py
Grava ticks em SQLite e JSONL para replay / análises.
"""
import sqlite3
import json
import time
import os
from pathlib import Path

DATA_DIR = os.path.join('data')
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
JSONL = os.path.join(DATA_DIR, 'ticks.jsonl')
DB_PATH = os.path.join(DATA_DIR, 'data.db')

_conn = None

def init_db():
    global _conn
    if _conn:
        return
    _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = _conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ticks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        round_id TEXT,
        tick_index INTEGER,
        multiplier REAL,
        button_enabled INTEGER,
        balance REAL,
        action INTEGER,
        reward REAL,
        img_path TEXT,
        meta TEXT
    )''')
    _conn.commit()

init_db()

def log_tick(round_id, tick_index, multiplier, button_enabled, balance, action, reward, img_path=None, meta=None):
    ts = time.strftime('%Y-%m-%dT%H:%M:%S')
    j = {'ts': ts, 'round_id': round_id, 'tick_index': tick_index, 'multiplier': multiplier, 'button_enabled': int(button_enabled) if button_enabled is not None else None, 'balance': balance, 'action': action, 'reward': reward, 'img_path': img_path, 'meta': meta}
    with open(JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(j) + '\n')
    c = _conn.cursor()
    c.execute('INSERT INTO ticks (ts,round_id,tick_index,multiplier,button_enabled,balance,action,reward,img_path,meta) VALUES (?,?,?,?,?,?,?,?,?,?)', (ts, round_id, tick_index, multiplier, int(button_enabled) if button_enabled is not None else None, balance, action, reward, img_path, json.dumps(meta)))
    _conn.commit()
