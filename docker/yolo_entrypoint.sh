#!/usr/bin/env bash
set -e

echo "🔹 Verifying ONNX Runtime GPU:"
python3 - <<'PY'
import onnxruntime as ort
print("ONNX Runtime:", ort.__version__)
providers = ort.get_available_providers()
print("Available providers:", providers)
PY

if [ ! -f "$YOLO_MODEL_PATH" ]; then
  echo "⚠️  Warning: YOLO model not found at $YOLO_MODEL_PATH"
fi

exec "$@"
