"""
run/collect.py
Modo shadow: captura e regista ticks SEM EFECTUAR toques.
"""
import time
import uuid
import os
from adb_utils import screencap_cv2
from perception import extract_features
from logger import log_tick

ROUND_ID_PREFIX = 'shadow'

def run_collect(iterations=None, delay=0.3):
    tick = 0
    round_id = f"{ROUND_ID_PREFIX}-{uuid.uuid4().hex[:8]}"
    while iterations is None or tick < iterations:
        img = screencap_cv2()
        feats = extract_features(img)
        # action None in shadow mode
        log_tick(round_id, tick, feats.get('multiplier'), feats.get('button_enabled'), feats.get('balance'), None, None, None)
        tick += 1
        time.sleep(delay)

if __name__ == '__main__':
    run_collect(iterations=200)

