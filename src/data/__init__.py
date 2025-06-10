"""
Resource management utilities for data directory.

Usage:
    from data import paths
    raw_video = paths.raw("game1.mp4")
    paths.ensure_dirs()
"""
from pathlib import Path

class _Paths:
    base = Path(__file__).parent

    def raw(self, *names):
        return self.base / "raw" / "/".join(names)

    def processed(self, *names):
        return self.base / "processed" / "/".join(names)

    def json_out(self, *names):
        return self.base / "outputs" / "json" / "/".join(names)

    def excel_out(self, *names):
        return self.base / "outputs" / "excel" / "/".join(names)

    def csv_out(self, *names):
        return self.base / "outputs" / "csv" / "/".join(names)

    def model(self, framework: str, filename: str):
        return self.base / "models" / framework / filename

    def ensure_dirs(self):
        for p in [
            self.base / "raw",
            self.base / "processed",
            self.base / "outputs/json",
            self.base / "outputs/excel",
            self.base / "outputs/csv",
            self.base / "models/yolo",
            self.base / "models/mediapipe",
        ]:
            p.mkdir(parents=True, exist_ok=True)

paths = _Paths()
