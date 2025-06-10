"""
query_api.py

FastAPI router exposing query endpoints.
"""

from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import crud, database

router = APIRouter()

@router.get("/recent_frames")
async def recent_frames(limit: int = 100, session: AsyncSession = Depends(database.get_session)):
    frames = await crud.get_event_frames(session, limit)
    return [f.__dict__ for f in frames]
