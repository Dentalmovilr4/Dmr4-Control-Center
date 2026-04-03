import json
import os
from datetime import datetime

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
        json.dump(history, f, indent=2)

def get_coin_history(history, name):
    results = []

    for snapshot in history:
        for coin in snapshot["coins"]:
            if coin["name"] == name:
                results.append(coin)

    return results[-10:]  # últimas 10 apariciones