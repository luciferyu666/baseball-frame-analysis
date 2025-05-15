import cv2, sys
from src.analysis.inference import detect_ball
from src.analysis.tracker import CentroidTracker
from src.annotation.overlay import draw
from src.storage.local_io import save

cap=cv2.VideoCapture(sys.argv[1])
tracker=CentroidTracker()
idx=0
while True:
    ret,f=cap.read()
    if not ret: break
    det=detect_ball(f)
    trk=tracker.update([(d['bbox'],d['conf']) for d in det])
    ov=draw(f,det,trk)
    save(ov,"offline")
    idx+=1
print("done")
