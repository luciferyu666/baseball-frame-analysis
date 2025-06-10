"""
database.py

Async SQLAlchemy engine + session for TimescaleDB (PostgreSQL) with asyncpg driver.
"""

from __future__ import annotations
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os

DATABASE_URI = os.getenv("DATABASE_URI", "postgresql+asyncpg://postgres:postgres@db:5432/baseball")

engine = create_async_engine(DATABASE_URI, echo=False, pool_size=5, max_overflow=5)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
