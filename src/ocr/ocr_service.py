"""
ocr_service.py

Region-based Tesseract OCR wrapper.

Dependencies
------------
pytesseract
opencv-python-headless
"""

from __future__ import annotations
import cv2
import numpy as np
import pytesseract
from typing import List, Dict, Tuple, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

def _prepare_image(img: np.ndarray) -> np.ndarray:
    """Basic preprocessing: grayscale, adaptive threshold."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thr = cv2.adaptiveThreshold(gray, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,
                                31, 2)
    return thr

def recognize_regions(frame: np.ndarray,
                      regions: Dict[str, Tuple[int, int, int, int]],
                      lang: str = "eng",
                      psm: int = 7) -> Dict[str, str]:
    """OCR on predefined regions.

    Parameters
    ----------
    frame : BGR image
    regions : dict mapping region_name -> (x1,y1,x2,y2)
    lang : tesseract language
    psm : tesseract page segmentation mode

    Returns
    -------
    dict region_name -> recognized text
    """
    results = {}
    for name, (x1, y1, x2, y2) in regions.items():
        roi = frame[y1:y2, x1:x2].copy()
        if roi.size == 0:
            results[name] = ""
            continue
        roi_prep = _prepare_image(roi)
        config = f"--psm {psm}"
        txt = pytesseract.image_to_string(roi_prep, lang=lang, config=config)
        results[name] = txt.strip()
        logger.debug("OCR %s: %s", name, txt.strip())
    return results

# ---------- Dynamic region detection (optional) ----------
def find_brightest_region(frame: np.ndarray, width: int = 400, height: int = 100) -> Tuple[int,int,int,int]:
    """Locate the brightest area (e.g., scoreboard) heuristically."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blur)
    x1 = max(max_loc[0] - width//2, 0)
    y1 = max(max_loc[1] - height//2, 0)
    x2 = min(x1 + width, frame.shape[1])
    y2 = min(y1 + height, frame.shape[0])
    return (x1, y1, x2, y2)

