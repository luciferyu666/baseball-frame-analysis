# Baseball Frame Analysis

End‑to‑end pipeline to **capture every video frame** from a baseball videogame, detect and track the pitched ball in real‑time,
annotate events, store them in a SQL database, and expose them through REST & WebSocket APIs.
Includes a lightweight React dashboard and CI/CD ready for Vercel & Docker.

```
# quick dev run
poetry install
docker compose up --build
```

Visit `http://localhost:8000/docs` for swagger and `http://localhost:5173` for live dashboard.
