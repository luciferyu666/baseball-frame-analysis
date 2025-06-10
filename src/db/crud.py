"""
crud.py

Basic CRUD operations using async SQLAlchemy.
"""

from __future__ import annotations
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from . import models

# ------------- EventFrame ---------------
async def add_event_frames(session: AsyncSession, frames: List[dict]):
    stmt = insert(models.EventFrame).values(frames)
    await session.execute(stmt)
    await session.commit()

async def get_event_frames(session: AsyncSession, limit: int = 100):
    result = await session.execute(select(models.EventFrame).order_by(models.EventFrame.id.desc()).limit(limit))
    return result.scalars().all()
