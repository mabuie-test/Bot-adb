"""
run/calibrate_rois.py
Rotina interativa simple para desenhar ROIs. Usa OpenCV GUI.
"""
import cv2
import adb_utils
import json
import os

OUT = os.path.join('configs', 'roi_config.json')

print('Abrindo browser no dispositivo (se GAME_URL estiver configurada, edite e reexecute se necessário).')
# Se quiser abrir URL automaticamente:
# adb_utils.open_url(os.environ.get('GAME_URL', 'https://seu-jogo.example.com/login'))

img = adb_utils.screencap_cv2()
clone = img.copy()

rois = ['multiplier', 'cashout_button', 'balance', 'stake_input']
cur = {'ix': -1, 'iy': -1, 'drawing': False, 'name': None, 'rects': {}}

def onmouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cur['ix'], cur['iy'] = x, y
        cur['drawing'] = True
    elif event == cv2.EVENT_MOUSEMOVE and cur['drawing']:
        img2 = clone.copy()
        cv2.rectangle(img2, (cur['ix'], cur['iy']), (x, y), (0,255,0), 2)
        cv2.imshow('calib', img2)
    elif event == cv2.EVENT_LBUTTONUP:
        cur['drawing'] = False
        x1, y1 = cur['ix'], cur['iy']
        x2, y2 = x, y
        cur['rects'][cur['name']] = [min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)]
        print('Saved', cur['name'], cur['rects'][cur['name']])

cv2.namedWindow('calib', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('calib', onmouse)

for name in rois:
    cur['name'] = name
    print('Desenhe ROI para', name, 'e carregue qualquer tecla quando terminar.')
    while True:
        cv2.imshow('calib', clone)
        k = cv2.waitKey(1) & 0xFF
        if name in cur['rects']:
            break

cv2.destroyAllWindows()

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(cur['rects'], f, indent=2, ensure_ascii=False)
print('Config de ROIs salva em', OUT)

