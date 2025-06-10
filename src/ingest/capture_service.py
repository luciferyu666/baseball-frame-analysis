"""
capture_service.py

Unified video capture interface for:
1. Local video files
2. Capture card / webcam devices
3. Network streams (RTSP / RTMP / HTTP MJPEG)

Dependencies
------------
opencv-python-headless
"""

from __future__ import annotations
import cv2
import threading
import queue
import time
import logging
from typing import Optional, Generator, Union

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

class StreamError(RuntimeError):
    """Raised when stream cannot be opened or read."""

class VideoCaptureService:
    """Threaded non‑blocking video capture.

    Examples
    --------
    >>> cap = VideoCaptureService(source="/path/to/file.mp4").start()
    >>> for frame in cap.frames():
    ...     # process
    ...     if cap.frame_id > 1000:
    ...         break
    >>> cap.stop()
    """

    def __init__(self,
                 source: Union[str, int],
                 queue_size: int = 256,
                 reconnect: bool = True):
        self.source = source
        self.queue_size = queue_size
        self.reconnect = reconnect

        self._cap: Optional[cv2.VideoCapture] = None
        self._q: queue.Queue = queue.Queue(maxsize=queue_size)
        self._thread: Optional[threading.Thread] = None
        self._stopped = threading.Event()
        self._paused = threading.Event()
        self.frame_id = 0

    # ---------------- Private helpers -----------------
    def _open(self) -> cv2.VideoCapture:
        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            raise StreamError(f"Cannot open source: {self.source}")
        return cap

    def _reader(self):
        logger.info("📺 Capture thread started for %s", self.source)
        while not self._stopped.is_set():
            if self._paused.is_set():
                time.sleep(0.05)
                continue
            ret, frame = self._cap.read()
            if not ret:
                logger.warning("End of stream or read failure on %s", self.source)
                if self.reconnect and isinstance(self.source, str) and self.source.startswith("rtsp"):
                    logger.info("Attempting to reconnect in 2 s...")
                    time.sleep(2)
                    self._cap.release()
                    try:
                        self._cap = self._open()
                        continue
                    except StreamError:
                        break
                else:
                    break
            try:
                self._q.put(frame, timeout=1)
                self.frame_id += 1
            except queue.Full:
                logger.debug("Frame queue full; dropping frame %s", self.frame_id)
        self._cap.release()
        logger.info("📺 Capture thread stopped for %s", self.source)

    # ---------------- Public API -----------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return self
        self._cap = self._open()
        self._stopped.clear()
        self._paused.clear()
        self._thread = threading.Thread(target=self._reader, daemon=True)
        self._thread.start()
        return self

    def pause(self):
        self._paused.set()

    def resume(self):
        self._paused.clear()

    def stop(self):
        self._stopped.set()
        if self._thread:
            self._thread.join(timeout=2)
        logger.info("Stopped capture service for %s", self.source)

    def read(self, timeout: float = 1.0):
        """Blocking read of next frame."""
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return None

    def frames(self) -> Generator:
        """Generator that yields frames as they become available."""
        while not self._stopped.is_set():
            frame = self.read(timeout=0.5)
            if frame is None:
                if not self._thread.is_alive():
                    break
                continue
            yield frame
