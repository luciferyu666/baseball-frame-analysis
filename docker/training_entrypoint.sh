#!/usr/bin/env bash
set -e

echo "🔹 Verifying PyTorch & MLflow:"
python3 - <<'PY'
import torch, mlflow, sys
print("Torch:", torch.__version__, "CUDA available:", torch.cuda.is_available())
print("MLflow:", mlflow.__version__)
PY

exec "$@"
