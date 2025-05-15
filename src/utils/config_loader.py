import os, pathlib, yaml
from functools import lru_cache

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

@lru_cache
def load_yaml(name: str):
    with open(BASE_DIR / "config" / name, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def env(key: str, default=None):
    return os.getenv(key, default)
