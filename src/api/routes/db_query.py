"""
db_query.py

/events/{game_id} route for querying stored events.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db

router = APIRouter()

@router.get("/events/{game_id}")
async def events(game_id: int, limit: int = 100,
                 session: AsyncSession = Depends(get_db)):
    if session is None:
        raise HTTPException(status_code=503, detail="DB not available")
    from db.crud import get_event_frames
    frames = await get_event_frames(session, limit=limit)
    return frames
