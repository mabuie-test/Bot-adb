"""
tools/analyze_logs.py
Análise simples dos logs gravados em data/ticks.jsonl e SQLite.
"""
import pandas as pd
from storage import fetch_ticks

def summary(n=10000):
    df = fetch_ticks(limit=n)
    if df.empty:
        print("Nenhum tick encontrado.")
        return
    grouped = df.groupby('round_id').agg(episode_reward=pd.NamedAgg(column='reward', aggfunc='sum'),
                                         steps=pd.NamedAgg(column='tick_index', aggfunc='max'))
    print("Episodes:", len(grouped))
    print("Avg episode reward:", grouped['episode_reward'].mean())
    print("Max episode reward:", grouped['episode_reward'].max())
    print(grouped.head())

if __name__ == '__main__':
    summary()

