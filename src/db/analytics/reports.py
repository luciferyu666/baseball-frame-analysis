"""
reports.py

Generate BI reports using pandas and matplotlib.
"""

from __future__ import annotations
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from ..integration.schema import FrameData

def pitch_speed_distribution(frames: List[FrameData], path: str):
    speeds = []
    for f in frames:
        for o in f.ocr:
            if "km/h" in o.text:
                try:
                    speed = int(o.text.split()[0])
                    speeds.append(speed)
                except ValueError:
                    continue
    if not speeds:
        return
    df = pd.DataFrame({"speed": speeds})
    ax = df.hist(bins=20)
    plt.title("Pitch Speed Distribution")
    plt.xlabel("km/h")
    plt.ylabel("Frequency")
    plt.savefig(path)
