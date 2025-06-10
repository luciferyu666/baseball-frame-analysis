"""
preprocess.py

Video preprocessing helpers:
1. FPS normalization
2. HDR ↔ SDR tone mapping

Requires ffmpeg CLI (system installed) for FPS conversion.
"""

from __future__ import annotations
import subprocess
import shutil
import cv2
import numpy as np
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

def _has_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None

# ---------------- FPS normalization ----------------
def normalize_fps(input_video: str,
                  output_video: str,
                  target_fps: int = 30,
                  codec: str = "libx264",
                  crf: int = 22):
    """Normalize a video's fps using ffmpeg."""
    if not _has_ffmpeg():
        raise EnvironmentError("ffmpeg not found in PATH")
    Path(output_video).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vf", f"fps={target_fps}",
        "-c:v", codec,
        "-crf", str(crf),
        "-preset", "veryfast",
        output_video
    ]
    logger.info("Running ffmpeg for FPS normalization: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)

# ---------------- HDR ↔ SDR conversion --------------
def tonemap_hdr_to_sdr(frame: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    """Simple gamma-based tonemapping from HDR (linear) to SDR."""
    frame = frame.astype(np.float32) / 65535.0  # assume 16‑bit HDR input
    frame = np.power(frame, 1.0 / gamma)
    frame = np.clip(frame * 255.0, 0, 255).astype(np.uint8)
    return frame

def tonemap_sdr_to_hdr(frame: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    """Approximate SDR → HDR expansion (inverse gamma)."""
    frame = frame.astype(np.float32) / 255.0
    frame = np.power(frame, gamma)
    frame = np.clip(frame * 65535.0, 0, 65535).astype(np.uint16)
    return frame

def convert_video_hdr_sdr(input_video: str,
                          output_video: str,
                          direction: str = "hdr_to_sdr",
                          target_fps: Optional[int] = None):
    """Convert full video HDR↔SDR using ffmpeg filters.

    direction: 'hdr_to_sdr' or 'sdr_to_hdr'
    """
    if not _has_ffmpeg():
        raise EnvironmentError("ffmpeg not found in PATH")
    Path(output_video).parent.mkdir(parents=True, exist_ok=True)
    vf_filters = []
    if direction == "hdr_to_sdr":
        # Use Hable tonemap for better quality
        vf_filters.append("zscale=t=linear,tonemap=tonemap=hable,zscale=t=bt709:m=bt709:r=tv")
    elif direction == "sdr_to_hdr":
        # Simple gamma re‑expansion to HDR10 PQ
        vf_filters.append("zscale=transfer=pq,format=yuv420p16le")
    else:
        raise ValueError("direction must be 'hdr_to_sdr' or 'sdr_to_hdr'")
    if target_fps:
        vf_filters.append(f"fps={target_fps}")
    filter_str = ",".join(vf_filters)
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-vf", filter_str,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        output_video
    ]
    logger.info("Running ffmpeg for HDR/SDR conversion: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)
