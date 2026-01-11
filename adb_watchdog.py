# adb_watchdog.py
import time
import subprocess
from adb_utils import list_devices, run_adb

CHECK_INTERVAL = 5.0  # segundos

def restart_adb_server():
    subprocess.run(['adb', 'kill-server'])
    time.sleep(0.5)
    subprocess.run(['adb', 'start-server'])

def monitor_loop():
    while True:
        try:
            devs = list_devices()
        except Exception:
            devs = []
        if not devs:
            # tenta restart
            print("[adb_watchdog] No devices found; restarting adb server")
            restart_adb_server()
            time.sleep(2)
        else:
            # OK
            # optionally print connected device
            print(f"[adb_watchdog] devices: {devs}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    monitor_loop()

