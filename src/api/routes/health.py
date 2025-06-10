"""
health.py

/health endpoint to check service status.
"""

from fastapi import APIRouter, Depends
from ..dependencies import get_detector, get_pose, get_ocr, get_db
import asyncio

router = APIRouter()

@router.get("/health")
async def health(detector = Depends(get_detector),
                 pose = Depends(get_pose),
                 ocr_func = Depends(get_ocr)):
    status = {"service": "ok"}
    status["detector_loaded"] = detector is not None
    status["pose_loaded"] = pose is not None
    status["ocr_ready"] = ocr_func is not None
    return status
