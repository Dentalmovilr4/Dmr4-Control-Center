import json
import os
from datetime import datetime

FILE = "data/history.json"

def ensure_directory():
    folder = os.path.dirname(FILE)
    if not os.path.exists(folder):
        os.makedirs(folder)

def load_history():
    ensure_directory()

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)

def save_snapshot(coins):
    ensure_directory()

    history = load_history()

    history.append({
        "timestamp": datetime.now().isoformat(),
        "coins": coins
    })

    with open(FILE, "w") as f:
        json.dump(history, f, indent=2)