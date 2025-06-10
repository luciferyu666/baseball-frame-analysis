"""
calibrate_frames.py

Check and adjust frame timestamps to ensure correct FPS alignment.
"""

from __future__ import annotations
import argparse, cv2, sys
from statistics import mean, stdev

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print("Cannot open video")
        sys.exit(1)

    timestamps=[]
    while True:
        ret, _ = cap.read()
        if not ret:
            break
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
    cap.release()

    diffs=[j-i for i,j in zip(timestamps[:-1],timestamps[1:])]
    avg=mean(diffs)
    sd=stdev(diffs) if len(diffs)>1 else 0
    target=1000/cap.get(cv2.CAP_PROP_FPS)

    print(f"Average frame interval: {avg:.2f} ms (target {target:.2f} ms)")
    print(f"Std dev: {sd:.2f} ms")
    if abs(avg-target)>1 or sd>1:
        print("⚠️  Frame timing drift detected, recommend re-encoding with fps filter")
    else:
        print("✅ Frame timing within tolerance")

if __name__ == "__main__":
    main()
