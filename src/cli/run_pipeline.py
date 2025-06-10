"""
run_pipeline.py

Execute full pipeline: ingest video -> detection, pose, ocr -> aggregate -> export JSON.

Example:
    python -m cli.run_pipeline --video input.mp4 --out data/outputs
"""
from __future__ import annotations
import argparse, os, cv2, sys, json
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Lazy imports to avoid heavy deps if modules missing
try:
    from detection.yolo_detector import YOLODetector
    from pose.pose_estimator import PoseEstimator
    from ocr.ocr_service import recognize_regions
    from integration.aggregator import StreamAggregator
    from integration.exporter import export_json
except ImportError as e:
    print("❌ Required modules missing:", e)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()

    Path(args.out).mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print("Cannot open video:", args.video)
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    detector = YOLODetector()
    pose_est = PoseEstimator()
    aggregator = StreamAggregator()

    frame_id = 0
    with tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            detections = detector.predict(frame)
            keypoints = [kp.__dict__ for kp in pose_est.infer(frame)]
            ocr_res = recognize_regions(frame, {})  # empty regions (placeholder)
            aggregator.add_frame(frame_id, detections, keypoints, ocr_res, datetime.utcnow())
            frame_id += 1
            pbar.update(1)

    cap.release()
    outfile = os.path.join(args.out, f"{Path(args.video).stem}_frames.json")
    export_json(aggregator.frames, outfile)
    print("✅ Pipeline finished, results saved to", outfile)

if __name__ == "__main__":
    main()
