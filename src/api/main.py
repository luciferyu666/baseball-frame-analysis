"""
main.py

Entry point for FastAPI service. Run with:
$ uvicorn api.main:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import inference, health, db_query

app = FastAPI(title="Baseball Frame Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inference.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(db_query.router, prefix="/api")
