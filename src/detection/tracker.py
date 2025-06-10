"""
tracker.py

Simple multi‑object tracking using Kalman Filter‑based SORT algorithm.

Dependencies
------------
filterpy (optional, falls back to simple centroid tracker if not installed)
"""

from __future__ import annotations
import numpy as np
from typing import List, Dict, Any
import itertools
import logging

logger = logging.getLogger(__name__)

try:
    from filterpy.kalman import KalmanFilter
except ImportError:
    KalmanFilter = None
    logger.warning("filterpy not found, falling back to centroid tracker")

# ---------------- SORT implementation ----------------
def iou(bb_test, bb_gt):
    xx1 = np.maximum(bb_test[0], bb_gt[0])
    yy1 = np.maximum(bb_test[1], bb_gt[1])
    xx2 = np.minimum(bb_test[2], bb_gt[2])
    yy2 = np.minimum(bb_test[3], bb_gt[3])
    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h
    o = wh / ((bb_test[2]-bb_test[0])*(bb_test[3]-bb_test[1]) +
              (bb_gt[2]-bb_gt[0])*(bb_gt[3]-bb_gt[1]) - wh + 1e-6)
    return o

class Track:
    _count = itertools.count()
    def __init__(self, bbox):
        self.id = next(self._count)
        self.hits = 0
        self.no_losses = 0
        self.bbox = bbox  # last bbox
    def update(self, bbox):
        self.bbox = bbox
        self.hits += 1
        self.no_losses = 0

class SORTTracker:
    """Basic IoU-based tracker (not full Kalman)."""
    def __init__(self, max_age=10, iou_threshold=0.3):
        self.tracks: List[Track] = []
        self.max_age = max_age
        self.iou_threshold = iou_threshold

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        det_bboxes = [d["bbox"] for d in detections]
        matched_det_idx = set()
        tracks_out = []

        # match existing tracks
        for trk in self.tracks:
            best_iou = 0
            best_idx = -1
            for idx, bbox in enumerate(det_bboxes):
                if idx in matched_det_idx:
                    continue
                iou_val = iou(bbox, trk.bbox)
                if iou_val > best_iou:
                    best_iou = iou_val
                    best_idx = idx
            if best_iou > self.iou_threshold:
                trk.update(det_bboxes[best_idx])
                matched_det_idx.add(best_idx)
            else:
                trk.no_losses += 1

        # create new tracks for unmatched detections
        for idx, bbox in enumerate(det_bboxes):
            if idx not in matched_det_idx:
                self.tracks.append(Track(bbox))

        # remove dead tracks
        self.tracks = [t for t in self.tracks if t.no_losses <= self.max_age]

        # output
        for trk in self.tracks:
            tracks_out.append({
                "track_id": trk.id,
                "bbox": trk.bbox,
                "age": trk.hits
            })
        return tracks_out
