# ⚾️ baseball-frame-analysis — Docker Deployment

This directory provides **production‑ready Docker assets** for the Baseball Frame Analysis system.
All images are GPU‑enabled but will fall back to CPU if no NVIDIA runtime is detected.

## 🖥️ Prerequisites
| Requirement | Version |
|-------------|---------|
| Docker      | 24.0+   |
| Docker Compose | v2.20+ |
| (Optional) NVIDIA Driver | 535+ |

```bash
# Verify docker & compose
docker -v
docker compose version
```

## 🚀 Build and Start

```bash
# From project root
cd baseball-frame-analysis/docker
docker compose build        # Build all images
docker compose up -d        # Start all containers in background
```

### Common Commands

| Action | Command |
|--------|---------|
| Stop stack | `docker compose down` |
| View logs  | `docker compose logs -f <service>` |
| Enter shell| `docker compose exec <service> bash` |
| Hot‑reload model | `docker compose restart yolo` |

## 🗂️ Service Overview

| Service  | Purpose                              |
|----------|--------------------------------------|
| ingest   | Video capture & preprocessing (OpenCV + FFmpeg) |
| yolo     | Real‑time object detection (YOLOv8 on ONNX Runtime) |
| training | Model fine‑tuning & MLflow tracking  |
| db       | PostgreSQL + TimescaleDB event store |

## 🔄 Hot Update Workflow
1. Run retraining inside `training` container (outputs new weights to `/models`).
2. `docker compose restart yolo` — YOLO container picks up new model without affecting others.

---

© 2025 Baseball‑AI Team
