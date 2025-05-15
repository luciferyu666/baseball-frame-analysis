## Architecture

1. **Capture Service** ingests RTSP or webcam frames and publishes them onto an in‑memory queue.
2. **API Service** pulls frames, performs inference, overlays results, stores events, and streams via WebSocket.
3. **Postgres** stores structured events; raw frames are optionally saved locally and synced to S3.

```
[Camera] -> [Capture] -> Queue -> [API (Inference+Overlay)] -> WebSocket -> Dashboard
                                   |
                                   +-> DB / Parquet / S3
```
