import json
import os
from datetime import datetime

FILE = "data/history.json"

def load_history():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)

def save_snapshot(results):
    history = load_history()

    history.append({
        "timestamp": str(datetime.now()),
        "coins": results
    })

    with open(FILE, "w") as f:
        json.dump(history[-50:], f, indent=2)