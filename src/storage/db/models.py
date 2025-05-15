from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import Integer, DateTime, JSON
Base = declarative_base()
class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frame_id: Mapped[int] = mapped_column(Integer)
    payload: Mapped[dict] = mapped_column(JSON)
import datetime   # ← 檔案上方若沒有就加
ts: Mapped[datetime.datetime] = mapped_column(DateTime)
