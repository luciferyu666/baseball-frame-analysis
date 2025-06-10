"""
swing_analysis.py

Detect swing start and end frames using wrist velocity
and classify Non‑Pitch (NP) events where no swing occurs.

Assumes keypoints from PoseEstimator.
"""

from __future__ import annotations
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class SwingEvent:
    start_frame: int
    end_frame: int
    duration_ms: float
    peak_velocity: float
    np_flag: bool

class SwingAnalyzer:
    def __init__(self,
                 fps: int = 30,
                 velocity_threshold: float = 800.0,  # px/s
                 min_duration_ms: int = 120,
                 max_duration_ms: int = 500):
        self.fps = fps
        self.vel_th = velocity_threshold
        self.min_dur = min_duration_ms
        self.max_dur = max_duration_ms

    def _wrist_velocity(self, wrist_positions: List[Tuple[float, float]]) -> List[float]:
        velocities = [0.0]
        for i in range(1, len(wrist_positions)):
            dx = wrist_positions[i][0] - wrist_positions[i-1][0]
            dy = wrist_positions[i][1] - wrist_positions[i-1][1]
            dist = np.hypot(dx, dy)
            velocities.append(dist * self.fps)  # px/s
        return velocities

    def analyze(self, frames_keypoints: List[List[Dict]]) -> List[SwingEvent]:
        """
        Parameters
        ----------
        frames_keypoints : list of keypoints per frame; a keypoint is dict with 'name','x','y'
        Returns
        -------
        list of SwingEvent
        """
        # Extract right wrist coords (or left if unavailable)
        wrist_positions = []
        for kp_list in frames_keypoints:
            wp = next((k for k in kp_list if k['name'] == 'RIGHT_WRIST'), None)
            if wp is None or wp['visibility'] < 0.3:
                wp = next((k for k in kp_list if k['name'] == 'LEFT_WRIST'), None)
            if wp:
                wrist_positions.append((wp['x'], wp['y']))
            else:
                wrist_positions.append(wrist_positions[-1] if wrist_positions else (0, 0))

        velocities = self._wrist_velocity(wrist_positions)
        events: List[SwingEvent] = []
        in_swing = False
        start_idx = 0
        peak_v = 0.0

        for i, v in enumerate(velocities):
            if not in_swing and v > self.vel_th:
                in_swing = True
                start_idx = i
                peak_v = v
            elif in_swing:
                peak_v = max(peak_v, v)
                if v < self.vel_th * 0.3 or i == len(velocities) - 1:
                    # end swing
                    duration = (i - start_idx) * (1000 / self.fps)
                    np_flag = not (self.min_dur <= duration <= self.max_dur)
                    events.append(SwingEvent(
                        start_frame=start_idx,
                        end_frame=i,
                        duration_ms=duration,
                        peak_velocity=peak_v,
                        np_flag=np_flag
                    ))
                    in_swing = False
        return events
