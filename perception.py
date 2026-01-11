"""
perception.py
Carrega ROIs e extrai features (multiplicador, saldo, botão) a partir da screenshot.
"""
import json
import os
import cv2
from ocr_utils import ocr_read_number, preprocess_for_ocr
import numpy as np

CFG_PATH = os.path.join('configs', 'roi_config.json')

def load_rois():
    with open(CFG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

ROIS = load_rois()

def crop(img, box):
    x1, y1, x2, y2 = box
    h, w = img.shape[:2]
    # clamp
    x1, x2 = max(0, x1), min(w, x2)
    y1, y2 = max(0, y1), min(h, y2)
    return img[y1:y2, x1:x2]

def detect_button(img, box, template=None, threshold=0.75):
    roi = crop(img, box)
    if roi is None or roi.size == 0:
        return False
    if template is not None:
        res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        _, maxv, _, _ = cv2.minMaxLoc(res)
        return maxv >= threshold
    else:
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        mean = gray.mean()
        # heurística: botão ativo costuma ser brilhante/destacado
        return mean > 100

def extract_features(img):
    features = {}
    # multiplier
    try:
        roi_mult = crop(img, ROIS['multiplier'])
        pre = preprocess_for_ocr(roi_mult)
        mult = ocr_read_number(pre)
        features['multiplier'] = mult
    except Exception:
        features['multiplier'] = None

    # balance
    try:
        roi_bal = crop(img, ROIS['balance'])
        pre = preprocess_for_ocr(roi_bal)
        bal = ocr_read_number(pre)
        features['balance'] = bal
    except Exception:
        features['balance'] = None

    # button
    try:
        btn = detect_button(img, ROIS['cashout_button'])
        features['button_enabled'] = bool(btn)
    except Exception:
        features['button_enabled'] = False

    return features

