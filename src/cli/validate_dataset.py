"""
validate_dataset.py

Validate dataset: HDR format, fps range, annotation consistency.
"""

from __future__ import annotations
import argparse, cv2, json, os, sys

def is_hdr(frame):
    return frame.dtype== "uint16" or frame.max()>255

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--videos_dir", required=True)
    parser.add_argument("--annotations", help="JSON annotations to validate")
    args=parser.parse_args()

    issues=[]
    for fn in os.listdir(args.videos_dir):
        if not fn.lower().endswith((".mp4",".mov",".mkv")):
            continue
        path=os.path.join(args.videos_dir, fn)
        cap=cv2.VideoCapture(path)
        if not cap.isOpened(): continue
        fps=cap.get(cv2.CAP_PROP_FPS)
        ret, frame=cap.read()
        hdr=is_hdr(frame) if ret else False
        if fps<24 or fps>120:
            issues.append(f"{fn}: unusual FPS {fps}")
        if hdr:
            issues.append(f"{fn}: HDR detected")
        cap.release()

    if args.annotations and os.path.exists(args.annotations):
        with open(args.annotations) as f:
            ann=json.load(f)
        for item in ann:
            if not os.path.exists(item["file"]):
                issues.append(f"Missing file in annotation: {item['file']}")

    if issues:
        print("⚠️  Dataset validation issues:")
        for i in issues: print(" -", i)
    else:
        print("✅ Dataset passed all checks.")

if __name__ == "__main__":
    main()
