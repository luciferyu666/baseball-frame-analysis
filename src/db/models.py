"""
models.py

SQLAlchemy ORM models for event frames and pose statistics.
"""

from __future__ import annotations
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
import datetime as _dt

class EventFrame(Base):
    __tablename__ = "event_frames"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frame_id: Mapped[int] = mapped_column(Integer, index=True)
    timestamp: Mapped[_dt.datetime] = mapped_column(DateTime, index=True)
    detections: Mapped[dict] = mapped_column(JSON)
    ocr: Mapped[dict] = mapped_column(JSON, default={})

class PoseStats(Base):
    __tablename__ = "pose_stats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frame_id: Mapped[int] = mapped_column(Integer, index=True)
    timestamp: Mapped[_dt.datetime] = mapped_column(DateTime, index=True)
    keypoints: Mapped[dict] = mapped_column(JSON)
