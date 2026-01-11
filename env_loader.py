# env_loader.py
from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parent
DOTENV = ROOT / '.env'

def init_env():
    if DOTENV.exists():
        load_dotenv(DOTENV)
    # defaults can be set here
    env = {
        'ADB_PATH': os.environ.get('ADB_PATH', 'adb'),
        'GAME_URL': os.environ.get('GAME_URL', ''),
        'DEVICE_SERIAL': os.environ.get('DEVICE_SERIAL', None),
        'TESSERACT_CMD': os.environ.get('TESSERACT_CMD', 'tesseract'),
    }
    return env

# usage: from env_loader import init_env; CFG = init_env()

