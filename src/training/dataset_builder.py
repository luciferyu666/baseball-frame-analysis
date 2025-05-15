from sqlalchemy.orm import Session
from src.storage.db.models import Event
from src.annotation.event_logger import engine
import json, pathlib

def export(export_dir="datasets/export"):
    pathlib.Path(export_dir).mkdir(parents=True, exist_ok=True)
    with Session(engine) as s:
        events = s.query(Event).all()
    with open(f"{export_dir}/events.jsonl","w") as f:
        for e in events:
            f.write(json.dumps({"frame_id":e.frame_id, **e.payload})+"\n")
    print("Export completed")
