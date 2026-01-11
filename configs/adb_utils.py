"""
adb_utils.py
Wrapper para ADB: screencap, tap, input_text, open_url, keyevent.
"""
import subprocess
import os

ADB = os.environ.get('ADB_PATH', 'adb')

def adb_run(cmd_list, timeout=None):
    return subprocess.run([ADB] + cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=timeout)

def screencap_cv2():
    """
    Captura a tela do dispositivo via `adb exec-out screencap -p`
    e devolve uma imagem OpenCV (BGR numpy array).
    """
    import numpy as np
    import cv2
    p = subprocess.Popen([ADB, 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
    img_bytes = p.stdout.read()
    if not img_bytes:
        raise RuntimeError("Nenhum dado recebido do adb screencap; verifica ligação ADB.")
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def tap(x, y):
    subprocess.run([ADB, 'shell', 'input', 'tap', str(int(x)), str(int(y))])

def input_text(text):
    safe = text.replace(' ', '%s')
    subprocess.run([ADB, 'shell', 'input', 'text', safe])

def keyevent(code):
    subprocess.run([ADB, 'shell', 'input', 'keyevent', str(code)])

def open_url(url):
    subprocess.run([ADB, 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', url])

