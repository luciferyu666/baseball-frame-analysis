"""
I/O helpers for images, videos, JSON, and Excel files.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
import cv2
import pandas as pd

# ---------- Image helpers ----------
def read_image(path: str):
    return cv2.imread(str(path), cv2.IMREAD_UNCHANGED)

def write_image(img, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), img)

# ---------- JSON helpers ----------
def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(data: Any, path: str, *, indent: int = 2):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

# ---------- Excel helpers ----------
def read_excel(path: str, sheet_name=0) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name)

def write_excel(df: pd.DataFrame, path: str, sheet_name: str = "Sheet1"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
