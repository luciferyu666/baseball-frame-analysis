# ⚾️ Baseball Frame Analysis — End‑to‑End System

A modular, container‑ready pipeline for **frame‑level video analytics** in baseball,
covering object detection (YOLOv8), pose estimation (MediaPipe), OCR, event aggregation,
database storage (TimescaleDB) and real‑time REST APIs (FastAPI).

## 🗂️ Project Layout

```
.
├─ docker/            # Container build files & compose stack
├─ src/               # Core source code (modular layers)
├─ data/              # Raw videos, processed frames, outputs, model weights
├─ mlruns/            # MLflow experiment tracking
├─ notebooks/         # Exploratory analysis & visualisation
└─ tests/             # Unit & integration test suites
```

## 🚀 Quick Start

```bash
# 1. Clone repo & enter
git clone <repo-url> && cd baseball-frame-analysis

# 2. Build & start services (GPU)
docker compose -f docker/docker-compose.yml up -d --build

# 3. Run pipeline on sample video
python -m src run_pipeline --video data/raw/sample.mp4 --out data/outputs
```

The full guide, including training pipelines, database dashboards
and API docs, is available in `/docs/architecture.md`.

## 🛠️ Environment

Copy `.env.example` to `.env` and set:

```env
DATABASE_URI=postgresql+asyncpg://postgres:postgres@db:5432/baseball
MLFLOW_TRACKING_URI=file:///workspace/mlruns
CUDA_VISIBLE_DEVICES=0
```

## 📄 License

Released under the MIT License. See `LICENSE` for details.
