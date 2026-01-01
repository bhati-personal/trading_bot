import json
import os

SEGMENT_FILE = "data/segments.json"


def load_segments():
    if not os.path.exists(SEGMENT_FILE):
        return {}
    with open(SEGMENT_FILE, "r") as f:
        return json.load(f)


def save_segments(segments: dict):
    os.makedirs(os.path.dirname(SEGMENT_FILE), exist_ok=True)
    with open(SEGMENT_FILE, "w") as f:
        json.dump(segments, f, indent=4)


def add_or_update_segment(name: str, lot_size: int):
    segments = load_segments()
    segments[name.upper()] = lot_size
    save_segments(segments)


def delete_segment(name: str):
    segments = load_segments()
    segments.pop(name.upper(), None)
    save_segments(segments)
