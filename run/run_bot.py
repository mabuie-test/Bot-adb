"""
run/run_bot.py
Loop principal: captura -> percepção -> decisão -> acção via ADB -> log.
ATENÇÃO: só execute depois de validar em shadow/collect.py e calibrar ROIs.
"""
import time
import os
import json
from adb_utils import screencap_cv2, tap, open_url
from perception import extract_features
from logger import log_tick
import yaml
from stable_baselines3 import PPO

CFG = yaml.safe_load(open(os.path.join('configs', 'agent_config.yaml'), 'r'))

MODEL_PATH = 'models/policy_latest'
# safety params
STAKE_MIN = CFG.get('safety', {}).get('stake_min', 0.5)
STAKE_MAX = CFG.get('safety', {}).get('stake_max', 5.0)
DAILY_TARGET = CFG.get('safety', {}).get('daily_target', 50.0)
DAILY_STOP_LOSS = CFG.get('safety', {}).get('daily_stop_loss', -50.0)

# load model if present
model = None
if os.path.exists(MODEL_PATH + '.zip'):
    model = PPO.load(MODEL_PATH)

round_id = 'live'
tick_index = 0

def safe_check(action, features):
    # Implementar regras hard: por exemplo, não permitir stake acima do máximo ou cashout falso
    # Aqui apenas devolve True; expandir conforme necessária lógica de risco.
    return True

if __name__ == '__main__':
    # opcional: abrir URL se necessário
    # open_url(os.environ.get('GAME_URL', 'https://seu-jogo.example.com/login'))
    time.sleep(2)
    while True:
        img = screencap_cv2()
        feats = extract_features(img)
        action = 0
        if model is not None:
            # construir observação simples (exemplo)
            obs = [feats.get('multiplier') or 1.0, 1.0 if feats.get('button_enabled') else 0.0]
            try:
                a, _ = model.predict(obs, deterministic=True)
                action = int(a)
            except Exception:
                action = 0

        if safe_check(action, feats):
            if action == 1 and feats.get('button_enabled'):
                rois = json.load(open('configs/roi_config.json', 'r', encoding='utf-8'))
                x1,y1,x2,y2 = rois['cashout_button']
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                tap(cx, cy)
        # log
        log_tick(round_id, tick_index, feats.get('multiplier'), feats.get('button_enabled'), feats.get('balance'), action, None)
        tick_index += 1
        time.sleep(0.25)
