#!/usr/bin/env bash
# Basic health‑check entrypoint for the ingest container

set -e

echo "🔹 OpenCV version:"
python3 - <<'PY'
import cv2, numpy as np, json, os
print("OpenCV‑Python:", cv2.__version__)
print("NumPy:", np.__version__)
print("Ingest container is ready. Mount your raw videos to /data/raw and preprocessing outputs to /data/processed.")
PY

# Keep container alive if no CMD provided
exec "$@"
