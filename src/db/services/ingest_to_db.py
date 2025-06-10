"""
ingest_to_db.py

Batch insert aggregated frame data into DB.
"""

from __future__ import annotations
from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..integration.schema import FrameData
from ..db import crud, database

async def ingest_frames(frames: List[FrameData], session: AsyncSession = Depends(database.get_session)):
    rows = [ {"frame_id": f.frame_id,
              "timestamp": f.timestamp,
              "detections": [d.dict() for d in f.detections],
              "ocr": [o.dict() for o in f.ocr] } for f in frames ]
    await crud.add_event_frames(session, rows)
    return {"inserted": len(rows)}
