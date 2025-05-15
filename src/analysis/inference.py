import cv2, numpy as np, torch
from src.utils.config_loader import load_yaml
cfg = load_yaml("model.yaml")

try:
    from ultralytics import YOLO
    _yolo = YOLO(cfg['weights'])
except Exception:
    _yolo = None

def detect_ball(frame):
    if _yolo:
        res = _yolo.predict(frame, verbose=False)[0]
        dets = []
        for b in res.boxes:
            if b.conf < cfg['confidence_threshold']:
                continue
            x1,y1,x2,y2 = map(int, b.xyxy[0])
            dets.append({"bbox":[x1,y1,x2,y2], "conf":float(b.conf)})
        return dets
    # fallback: simple colour threshold
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,0,200), (180,40,255))
    cnts,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dets=[]
    for c in cnts:
        if cv2.contourArea(c)<60:
            continue
        x,y,w,h = cv2.boundingRect(c)
        dets.append({"bbox":[x,y,x+w,y+h], "conf":1.0})
    return dets
