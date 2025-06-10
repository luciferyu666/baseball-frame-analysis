"""
yolo_detector.py

YOLOv8 ONNX inference wrapper.

Requirements
------------
onnxruntime-gpu  (or onnxruntime for CPU)
ultralytics      (for preprocessing helpers; optional)

Environment variable
--------------------
YOLO_MODEL_PATH : path to .onnx weights
"""

from __future__ import annotations
import os
import time
import cv2
import numpy as np
import onnxruntime as ort
from typing import List, Dict, Any

class YOLODetector:
    """Lightweight ONNX Runtime wrapper for YOLOv8."""

    def __init__(self,
                 model_path: str | None = None,
                 conf_thres: float = 0.25,
                 iou_thres: float = 0.45,
                 input_size: int = 640,
                 providers: list[str] | None = None):
        self.model_path = model_path or os.getenv("YOLO_MODEL_PATH", "yolov8.onnx")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"YOLO model not found: {self.model_path}")
        self.session = ort.InferenceSession(self.model_path,
                                            providers=providers or ["CUDAExecutionProvider", "CPUExecutionProvider"])
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.input_size = input_size
        self._input_name = self.session.get_inputs()[0].name

    # -------------- preprocess -------------------
    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        h, w = img.shape[:2]
        scale = self.input_size / max(h, w)
        nh, nw = int(h * scale), int(w * scale)
        resized = cv2.resize(img, (nw, nh))
        padded = np.zeros((self.input_size, self.input_size, 3), dtype=np.uint8)
        padded[:nh, :nw] = resized
        img_in = padded[:, :, ::-1].transpose(2, 0, 1)  # BGR → RGB, HWC → CHW
        img_in = img_in.astype(np.float32) / 255.0
        img_in = np.expand_dims(img_in, 0)
        return img_in, scale, (nw, nh)

    # -------------- postprocess ------------------
    def _nms(self, boxes, scores, iou_threshold):
        # Pure python NMS
        idxs = scores.argsort()[::-1]
        keep = []
        while idxs.size > 0:
            i = idxs[0]
            keep.append(i)
            xx1 = np.maximum(boxes[i, 0], boxes[idxs[1:], 0])
            yy1 = np.maximum(boxes[i, 1], boxes[idxs[1:], 1])
            xx2 = np.minimum(boxes[i, 2], boxes[idxs[1:], 2])
            yy2 = np.minimum(boxes[i, 3], boxes[idxs[1:], 3])
            inter = np.maximum(0, xx2 - xx1) * np.maximum(0, yy2 - yy1)
            iou = inter / ( (boxes[i, 2] - boxes[i, 0]) * (boxes[i, 3] - boxes[i, 1]) + 
                            (boxes[idxs[1:], 2] - boxes[idxs[1:], 0]) * (boxes[idxs[1:], 3] - boxes[idxs[1:], 1]) - inter + 1e-6 )
            idxs = idxs[1:][iou < iou_threshold]
        return keep

    # -------------- public predict ---------------
    def predict(self, img: np.ndarray) -> List[Dict[str, Any]]:
        img_in, scale, (nw, nh) = self._preprocess(img)
        start = time.time()
        outputs = self.session.run(None, {self._input_name: img_in})[0]  # (batch, boxes, 85)
        infer_ms = (time.time() - start) * 1000

        outputs = np.squeeze(outputs, 0)
        scores = outputs[:, 4] * outputs[:, 5:].max(axis=1)
        mask = scores >= self.conf_thres
        outputs = outputs[mask]
        scores = scores[mask]
        if outputs.size == 0:
            return []
        boxes = outputs[:, :4]
        # xywh → xyxy in resized space
        boxes[:, :2] -= boxes[:, 2:] / 2
        boxes[:, 2:] += boxes[:, :2]
        # map back to original resolution
        boxes /= scale
        classes = outputs[:, 5:].argmax(axis=1)

        keep = self._nms(boxes, scores, self.iou_thres)
        results = []
        for i in keep:
            x1, y1, x2, y2 = boxes[i]
            results.append({
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "confidence": float(scores[i]),
                "class_id": int(classes[i])
            })
        return results
