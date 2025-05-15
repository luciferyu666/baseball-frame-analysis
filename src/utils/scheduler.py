from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
import shutil, pathlib, time

scheduler = BackgroundScheduler()

def cleanup_outputs():
    out_dir = pathlib.Path("outputs")
    if not out_dir.exists():
        return
    for f in out_dir.glob("*.jpg"):
        # 24h retention
        if time.time() - f.stat().st_mtime > 86400:
            f.unlink()
            logger.info(f"Removed old output {f}")

scheduler.add_job(cleanup_outputs, "interval", hours=1)
def start():
    scheduler.start()
