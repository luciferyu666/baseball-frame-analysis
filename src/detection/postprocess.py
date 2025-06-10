"""
postprocess.py

Extra postprocessing utilities:
1. Non‑maximum suppression
2. Event type tagging (rule‑based)
"""

from __future__ import annotations
import numpy as np
from typing import List, Dict, Any

# ------------- NMS helper --------------
def nms_boxes(dets: List[Dict[str, Any]],
              iou_threshold: float = 0.5) -> List[Dict[str, Any]]:
    if not dets:
        return []
    boxes = np.array([d["bbox"] for d in dets])
    scores = np.array([d["confidence"] for d in dets])
    idxs = scores.argsort()[::-1]
    keep_idx = []
    while idxs.size > 0:
        i = idxs[0]
        keep_idx.append(i)
        xx1 = np.maximum(boxes[i, 0], boxes[idxs[1:], 0])
        yy1 = np.maximum(boxes[i, 1], boxes[idxs[1:], 1])
        xx2 = np.minimum(boxes[i, 2], boxes[idxs[1:], 2])
        yy2 = np.minimum(boxes[i, 3], boxes[idxs[1:], 3])
        inter = np.maximum(0, xx2 - xx1) * np.maximum(0, yy2 - yy1)
        iou = inter / ((boxes[i, 2]-boxes[i, 0]) * (boxes[i, 3]-boxes[i, 1]) +
                       (boxes[idxs[1:], 2]-boxes[idxs[1:], 0]) * (boxes[idxs[1:], 3]-boxes[idxs[1:], 1]) -
                       inter + 1e-6)
        idxs = idxs[1:][iou < iou_threshold]
    return [dets[i] for i in keep_idx]

# --------- Event tagging example -------
def tag_events(dets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Simple rule‑based event tagging.

    Example rules:
    class_id 0: ball
    class_id 1: bat
    class_id 2: player
    If ball and bat overlap IoU > 0.2 → 'contact'
    """
    # find indices of ball & bat
    balls = [d for d in dets if d.get("class_id") == 0]
    bats = [d for d in dets if d.get("class_id") == 1]
    events = []
    for ball in balls:
        bx1, by1, bx2, by2 = ball["bbox"]
        for bat in bats:
            x1 = max(bx1, bat["bbox"][0])
            y1 = max(by1, bat["bbox"][1])
            x2 = min(bx2, bat["bbox"][2])
            y2 = min(by2, bat["bbox"][3])
            inter = max(0, x2 - x1) * max(0, y2 - y1)
            area_ball = (bx2 - bx1) * (by2 - by1)
            area_bat = (bat["bbox"][2] - bat["bbox"][0]) * (bat["bbox"][3] - bat["bbox"][1])
            iou = inter / (area_ball + area_bat - inter + 1e-6)
            if iou > 0.2:
                events.append({
                    "type": "contact",
                    "ball": ball,
                    "bat": bat,
                    "iou": iou
                })
    return events
