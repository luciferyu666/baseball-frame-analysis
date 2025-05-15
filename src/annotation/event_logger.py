import datetime, json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.storage.db.models import Base, Event
from src.utils.config_loader import env

engine = create_engine(env("DATABASE_URL", "sqlite:///./events.db"), future=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def log(frame_id:int, detections, tracks):
    with Session() as s:
        e = Event(frame_id=frame_id,
                  payload={"detections":detections,"tracks":{k:list(v) for k,v in tracks.items()}},
                  ts=datetime.datetime.utcnow())
        s.add(e)
        s.commit()
