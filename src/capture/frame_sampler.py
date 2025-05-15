"""Utility to downsample frames from the global queue at a target FPS."""
import time, queue
def sampler(frame_queue: queue.Queue, target_fps: int):
    delay = 1.0 / target_fps
    last = 0
    while True:
        now = time.time()
        if now - last < delay:
            time.sleep(delay / 2)
            continue
        try:
            frame = frame_queue.get(timeout=0.1)
            last = now
            yield frame
        except queue.Empty:
            continue
