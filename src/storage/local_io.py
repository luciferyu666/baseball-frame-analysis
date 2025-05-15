import cv2, pathlib, datetime
OUT_DIR = pathlib.Path("outputs"); OUT_DIR.mkdir(exist_ok=True)
def save(frame, prefix="frame"):
    ts = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    path = OUT_DIR / f"{prefix}_{ts}.jpg"
    cv2.imwrite(str(path), frame)
    return path
