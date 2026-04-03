import json
from datetime import datetime
import os

FILE = "data/history.json"

def load_history():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)

def save_snapshot(coins):
    history = load_history()

    history.append({
        "timestamp": datetime.now().isoformat(),
        "coins": coins
    })

    with open(FILE, "w") as f:
        json.dump(history, f, indent=2)1