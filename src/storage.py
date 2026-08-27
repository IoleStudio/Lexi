import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_words():
    with (DATA_DIR / "words.txt").open(encoding="utf-8") as f:
        return f.read().splitlines()

def load_stats():
    with (DATA_DIR / "stats.json").open("r", encoding="utf-8") as f:
        return json.load(f)

def save_stats(data):
    with (DATA_DIR / "stats.json").open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)