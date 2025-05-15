import cv2, datetime, pathlib, os
from src.utils.config_loader import load_yaml
cfg = load_yaml("capture.yaml")
RESOLUTION = tuple(cfg['resolution'])

def record(frame_iter, out_dir="recordings"):
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    writer = cv2.VideoWriter(f"{out_dir}/{now}.mp4",
                             cv2.VideoWriter_fourcc(*'mp4v'),
                             cfg['fps'], RESOLUTION)
    for frame in frame_iter:
        writer.write(frame)
    writer.release()
