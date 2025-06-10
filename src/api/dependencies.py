"""
dependencies.py

Provides shared instances of models and DB session for FastAPI DI.
"""

from __future__ import annotations
from functools import lru_cache
from fastapi import Depends
from typing import AsyncGenerator
import asyncio

# Attempt to import components; fall back to None
try:
    from detection.yolo_detector import YOLODetector
    yolo_detector = YOLODetector()
except Exception:
    yolo_detector = None

try:
    from pose.pose_estimator import PoseEstimator
    pose_estimator = PoseEstimator()
except Exception:
    pose_estimator = None

try:
    from ocr.ocr_service import recognize_regions
except Exception:
    recognize_regions = None

# Database session
async def get_db():
    try:
        from db.database import get_session
        async for sess in get_session():
            yield sess
    except ImportError:
        # Dummy async generator
        async def dummy():
            yield None
        async for _ in dummy():
            return

def get_detector():
    return yolo_detector

def get_pose():
    return pose_estimator

def get_ocr():
    return recognize_regions
