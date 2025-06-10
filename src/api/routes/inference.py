"""
inference.py

/inference endpoint: accepts image file upload and returns detection + pose + ocr.
"""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import cv2
import numpy as np
import tempfile
from ..dependencies import get_detector, get_pose, get_ocr

router = APIRouter()

@router.post("/inference")
async def inference_endpoint(file: UploadFile = File(...),
                             detector = Depends(get_detector),
                             pose = Depends(get_pose),
                             ocr_func = Depends(get_ocr)):
    data = await file.read()
    img_arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    detections = detector.predict(img) if detector else []
    keypoints = [k.__dict__ for k in pose.infer(img)] if pose else []
    ocr_res = ocr_func(img, {}) if ocr_func else {}

    return {"detections": detections,
            "pose": keypoints,
            "ocr": ocr_res}
