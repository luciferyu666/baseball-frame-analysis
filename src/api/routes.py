from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.storage.db.models import Event
from src.annotation.event_logger import engine
router = APIRouter()

def get_db():
    with Session(engine) as s:
        yield s

@router.get("/events")
def list_events(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    return db.query(Event).offset(skip).limit(limit).all()
