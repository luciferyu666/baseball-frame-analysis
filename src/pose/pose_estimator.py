"""
pose_estimator.py

Wrapper around MediaPipe Pose for extracting human skeleton keypoints.

Dependencies
------------
mediapipe>=0.10
opencv-python-headless
"""

from __future__ import annotations
import cv2
import numpy as np
import mediapipe as mp
from dataclasses import dataclass
from typing import List, Dict, Tuple

mp_pose = mp.solutions.pose

@dataclass
class Keypoint:
    name: str
    x: float
    y: float
    z: float
    visibility: float

class PoseEstimator:
    def __init__(self,
                 static_image_mode: bool = False,
                 model_complexity: int = 1,
                 detection_confidence: float = 0.5,
                 tracking_confidence: float = 0.5):
        self.pose = mp_pose.Pose(static_image_mode=static_image_mode,
                                 model_complexity=model_complexity,
                                 min_detection_confidence=detection_confidence,
                                 min_tracking_confidence=tracking_confidence)

    def infer(self, frame: np.ndarray) -> List[Keypoint]:
        """
        Perform pose estimation on a single BGR frame.

        Returns
        -------
        List[Keypoint]
            All 33 body keypoints with normalized coordinates (0‑1) and visibility.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)
        if not result.pose_landmarks:
            return []
        keypoints = []
        h, w = frame.shape[:2]
        for i, lm in enumerate(result.pose_landmarks.landmark):
            keypoints.append(Keypoint(
                name=mp_pose.PoseLandmark(i).name,
                x=lm.x * w,
                y=lm.y * h,
                z=lm.z * w,           # scale depth by width
                visibility=lm.visibility
            ))
        return keypoints

    def close(self):
        self.pose.close()
