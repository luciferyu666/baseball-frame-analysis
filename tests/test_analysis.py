import cv2, numpy as np
from src.analysis.inference import detect_ball
def test_detect():
    img=np.zeros((100,100,3),dtype=np.uint8)
    dets=detect_ball(img)
    assert isinstance(dets,list)
