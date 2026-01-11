"""
ocr_utils.py
Pré-processamento OpenCV e leitura com pytesseract para números.
"""
import cv2
import pytesseract
import numpy as np
import re

def preprocess_for_ocr(img):
    # recebe BGR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    if h < 40:
        factor = max(2.0, 40.0 / max(1, h))
        gray = cv2.resize(gray, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    th = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((2,2), np.uint8)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    return th

def ocr_read_number(img):
    """
    img: imagem preprocessada (grayscale / binary)
    devolve float ou None
    """
    config = '--psm 7 -c tessedit_char_whitelist=0123456789.,'
    text = pytesseract.image_to_string(img, config=config)
    if not text:
        return None
    text = text.strip().replace(',', '.')
    m = re.search(r'(\d+\.?\d*)', text)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

