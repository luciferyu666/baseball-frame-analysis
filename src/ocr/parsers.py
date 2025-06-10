"""
parsers.py

Parsing helper functions for OCR text outputs.
"""

from __future__ import annotations
import re
from typing import Dict, Any, Optional, Tuple

# ------------- ball speed ------------------
def parse_ball_speed(text: str) -> Optional[int]:
    """Extract ball speed (km/h or mph) from text."""
    m = re.search(r"(\d{2,3})\s*(?:km/h|kph|mph)?", text.lower())
    if m:
        return int(m.group(1))
    return None

# ------------- scoreboard -------------------
def parse_scoreboard(text: str) -> Dict[str, Any]:
    """Parse scoreboard like 'H 2  E 0  S 3' etc.

    Returns
    -------
    dict with keys hits, errors, strikes if found.
    """
    result = {}
    pairs = {"h": "hits", "e": "errors", "s": "strikes", "b": "balls"}
    for key, name in pairs.items():
        m = re.search(key + r"\s*(\d+)", text.lower())
        if m:
            result[name] = int(m.group(1))
    return result

# ------------- team names / inning ----------
def parse_team_names(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract two uppercase team abbreviations (max 4 letters)."""
    m = re.findall(r"\b([A-Z]{2,4})\b", text)
    if len(m) >= 2:
        return m[0], m[1]
    return None, None
