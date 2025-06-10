"""
schema.py

Pydantic models describing unified frame data and events.
"""

from __future__ import annotations
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional
from datetime import datetime

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @validator("x2")
    def x2_gt_x1(cls, v, values):
        if "x1" in values and v <= values["x1"]:
            raise ValueError("x2 must be greater than x1")
        return v

    @validator("y2")
    def y2_gt_y1(cls, v, values):
        if "y1" in values and v <= values["y1"]:
            raise ValueError("y2 must be greater than y1")
        return v

class DetectionObject(BaseModel):
    bbox: BoundingBox
    confidence: float = Field(..., ge=0, le=1)
    class_id: int
    track_id: Optional[int] = None

class Keypoint(BaseModel):
    name: str
    x: float
    y: float
    z: float = 0.0
    visibility: float = Field(..., ge=0, le=1)

class PoseFrame(BaseModel):
    keypoints: List[Keypoint]

class OCRField(BaseModel):
    region: str
    text: str

class FrameData(BaseModel):
    frame_id: int
    timestamp: datetime
    detections: List[DetectionObject] = []
    pose: Optional[PoseFrame] = None
    ocr: List[OCRField] = []

class Event(BaseModel):
    type: str
    frame_start: int
    frame_end: int
    metadata: dict
