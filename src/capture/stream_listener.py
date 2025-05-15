import cv2, queue, threading, os
from loguru import logger
from src.utils.config_loader import env, load_yaml

cfg = load_yaml("capture.yaml")
FPS = int(env("FPS", cfg['fps']))
STREAM_URL = env("STREAM_URL", "0")
FRAME_QUEUE = queue.Queue(maxsize=cfg['queue_size'])

def _capture():
    cap = cv2.VideoCapture(0 if STREAM_URL.isdigit() else STREAM_URL)
    if not cap.isOpened():
        logger.error(f"Cannot open stream {STREAM_URL}")
        return
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        try:
            FRAME_QUEUE.put(frame, timeout=1)
        except queue.Full:
            logger.debug("Frame queue full; dropping frame")

def start():
    threading.Thread(target=_capture, daemon=True).start()
    logger.info("Capture started")

if __name__ == "__main__":
    start()
    import time
    while True:
        if not FRAME_QUEUE.empty():
            f = FRAME_QUEUE.get()
            logger.info(f"Got frame {f.shape}")
        time.sleep(1.0/FPS)
