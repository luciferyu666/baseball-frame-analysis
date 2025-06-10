"""
Utility functions for timestamp handling, coordinate conversion, and error smoothing.
"""

from __future__ import annotations
import datetime as _dt
import time as _time
from typing import List, Tuple, Sequence, Union, Optional

def to_timestamp(dt: Union[_dt.datetime, None] = None, tz: str = "utc") -> float:
    """
    Convert a datetime object to POSIX timestamp (float seconds).

    If *dt* is None, current time is used.
    """
    if dt is None:
        dt = _dt.datetime.utcnow()
    if tz.lower() == "local":
        return dt.timestamp()
    return dt.replace(tzinfo=_dt.timezone.utc).timestamp()

def timestamp_to_iso(ts: float, tz: str = "utc") -> str:
    """
    Convert POSIX timestamp to ISO‑8601 string.

    Parameters
    ----------
    ts : float
        Seconds since epoch.
    tz : str
        "utc" (default) or "local".
    """
    if tz.lower() == "local":
        dt = _dt.datetime.fromtimestamp(ts)
    else:
        dt = _dt.datetime.utcfromtimestamp(ts)
    return dt.isoformat(timespec="milliseconds") + ("Z" if tz.lower() == "utc" else "")

def abs_to_rel(x: float, y: float, width: int, height: int) -> Tuple[float, float]:
    """
    Convert absolute pixel coordinates to relative (0‑1) values.
    """
    return x / width, y / height

def rel_to_abs(rx: float, ry: float, width: int, height: int) -> Tuple[int, int]:
    """
    Convert relative coordinates (0‑1) to absolute pixel coordinates.
    """
    return int(rx * width), int(ry * height)

def calibrate_error(value: float, offset: float = 0.0, scale: float = 1.0) -> float:
    """
    Apply linear calibration to correct systematic error.
    """
    return (value + offset) * scale

def smooth_coordinates(coords: Sequence[Tuple[float, float]],
                        window: int = 5) -> List[Tuple[float, float]]:
    """
    Simple moving average smoothing of a list of (x, y) coordinates.

    Parameters
    ----------
    coords : list of (x, y)
    window : size of averaging window

    Returns
    -------
    smoothed list of (x, y)
    """
    if window <= 1:
        return list(coords)
    smoothed = []
    buff_x, buff_y = [], []
    for i, (x, y) in enumerate(coords):
        buff_x.append(x)
        buff_y.append(y)
        if len(buff_x) > window:
            buff_x.pop(0)
            buff_y.pop(0)
        smoothed.append((sum(buff_x) / len(buff_x), sum(buff_y) / len(buff_y)))
    return smoothed
