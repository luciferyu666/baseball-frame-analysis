"""
aggregator.py

Combine outputs from detection, pose, and OCR into a time‑series stream.
"""

from __future__ import annotations
from typing import List, Optional
from datetime import datetime, timedelta
from .schema import FrameData, DetectionObject, PoseFrame, OCRField, Event
import logging

logger = logging.getLogger(__name__)

class StreamAggregator:
    def __init__(self):
        self.frames: List[FrameData] = []

    def add_frame(self,
                  frame_id: int,
                  detections: Optional[List[dict]] = None,
                  pose: Optional[List[dict]] = None,
                  ocr: Optional[dict] = None,
                  timestamp: Optional[datetime] = None):
        """
        Add a single frame's data from modules.

        Parameters
        ----------
        detections : list of dict produced by detection module
        pose       : list of keypoint dicts
        ocr        : dict of region_name -> text
        """
        fd = FrameData(
            frame_id=frame_id,
            timestamp=timestamp or datetime.utcnow(),
            detections=[DetectionObject(**d) for d in (detections or [])],
            pose=PoseFrame(keypoints=[k for k in (pose or [])]) if pose else None,
            ocr=[OCRField(region=k, text=v) for k, v in (ocr or {}).items()]
        )
        self.frames.append(fd)

    # Example: derive simple events
    def generate_contact_events(self, iou_thres: float = 0.2) -> List[Event]:
        events = []
        for f in self.frames:
            balls = [d for d in f.detections if d.class_id == 0]
            bats = [d for d in f.detections if d.class_id == 1]
            for ball in balls:
                for bat in bats:
                    iou = self._bbox_iou(ball.bbox, bat.bbox)
                    if iou > iou_thres:
                        events.append(Event(
                            type="contact",
                            frame_start=f.frame_id,
                            frame_end=f.frame_id,
                            metadata={"iou": iou,
                                      "ball_track": ball.track_id,
                                      "bat_track": bat.track_id}
                        ))
        return events

    @staticmethod
    def _bbox_iou(b1, b2) -> float:
        xx1 = max(b1.x1, b2.x1)
        yy1 = max(b1.y1, b2.y1)
        xx2 = min(b1.x2, b2.x2)
        yy2 = min(b1.y2, b2.y2)
        w = max(0.0, xx2 - xx1)
        h = max(0.0, yy2 - yy1)
        inter = w * h
        union = b1.width * b1.height + b2.width * b2.height - inter + 1e-6
        return inter / union
