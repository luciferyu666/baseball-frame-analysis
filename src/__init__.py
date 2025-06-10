"""Baseball Frame Analysis SDK

This package exposes high‑level helpers to invoke the end‑to‑end pipeline programmatically.

Example
-------
>>> from src import run
>>> run(video="data/raw/sample.mp4", out_dir="data/outputs")
"""

__version__ = "1.0.0"

def run(video: str, out_dir: str = "data/outputs"):
    """Convience wrapper to execute CLI run_pipeline programmatically."""
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "cli.run_pipeline", "--video", video, "--out", out_dir], check=True)
