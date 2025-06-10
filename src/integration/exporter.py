"""
exporter.py

Export integrated data to JSON / CSV / Excel and expose an optional FastAPI router.
"""

from __future__ import annotations
import json
from typing import List
from pathlib import Path
import pandas as pd
from fastapi import APIRouter
from .schema import FrameData, Event
import logging

logger = logging.getLogger(__name__)

def frames_to_dataframe(frames: List[FrameData]) -> pd.DataFrame:
    rows = []
    for f in frames:
        for det in f.detections:
            rows.append({
                "frame_id": f.frame_id,
                "timestamp": f.timestamp.isoformat(),
                "class_id": det.class_id,
                "track_id": det.track_id,
                "x1": det.bbox.x1,
                "y1": det.bbox.y1,
                "x2": det.bbox.x2,
                "y2": det.bbox.y2,
                "conf": det.confidence
            })
    return pd.DataFrame(rows)

def export_json(data: List[FrameData], path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([d.dict() for d in data], f, ensure_ascii=False, indent=2)
    logger.info("Exported JSON to %s", path)

def export_csv(frames: List[FrameData], path: str):
    df = frames_to_dataframe(frames)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info("Exported CSV to %s", path)

def export_excel(frames: List[FrameData], path: str):
    df = frames_to_dataframe(frames)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False)
    logger.info("Exported Excel to %s", path)

# ------------- FastAPI Router ---------------
def create_router(frames: List[FrameData]) -> APIRouter:
    router = APIRouter()

    @router.get("/frames")
    async def get_frames():
        return [f.dict() for f in frames]

    return router
