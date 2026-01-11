# adb_utils.py  (revisado)
import os
import subprocess
import time
from env_loader import init_env

CFG = init_env()
ADB = CFG.get('ADB_PATH', 'adb')
DEVICE_SERIAL = os.environ.get('DEVICE_SERIAL') or None

def _adb_cmd(args):
    """
    Internal: return command list for adb; includes -s DEVICE if specified.
    """
    base = [ADB]
    if DEVICE_SERIAL:
        base += ['-s', DEVICE_SERIAL]
    base += args
    return base

def run_adb(args, timeout=30):
    cmd = _adb_cmd(args)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return proc

def list_devices():
    proc = run_adb(['devices'])
    out = proc.stdout.decode(errors='ignore')
    lines = out.strip().splitlines()
    devices = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == 'device':
            devices.append(parts[0])
    return devices

def check_adb():
    """
    Returns True if adb responds and at least one device connected.
    """
    try:
        devs = list_devices()
        return len(devs) > 0
    except Exception:
        return False

def screencap_cv2(retries=2, timeout=10):
    """
    Capture screen via 'adb exec-out screencap -p' and return OpenCV BGR array.
    """
    import numpy as np
    import cv2
    for attempt in range(retries):
        try:
            proc = subprocess.Popen(_adb_cmd(['exec-out', 'screencap', '-p']), stdout=subprocess.PIPE)
            img_bytes = proc.stdout.read()
            if not img_bytes:
                raise RuntimeError("Empty screenshot bytes")
            arr = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            time.sleep(0.5)
            if attempt == retries - 1:
                raise
    raise RuntimeError("screencap failed")

def tap(x, y):
    run_adb(['shell', 'input', 'tap', str(int(x)), str(int(y))])

def input_text(text):
    safe = text.replace(' ', '%s')
    run_adb(['shell', 'input', 'text', safe])

def keyevent(code):
    run_adb(['shell', 'input', 'keyevent', str(code)])

def open_url(url):
    run_adb(['shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', url])

def pull(path_on_device, dest_local):
    run_adb(['pull', path_on_device, dest_local])

def push(local, dest_on_device):
    run_adb(['push', local, dest_on_device])
