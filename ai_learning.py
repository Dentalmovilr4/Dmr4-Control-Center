import json
import os

FILE = "data/history.json"

def load_history():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def evaluate_past_performance():
    history = load_history()

    if len(history) < 2:
        return {}

    performance = {}

    # comparar snapshots
    for i in range(len(history) - 1):
        current = history[i]["coins"]
        future = history[i + 1]["coins"]

        future_map = {c["name"]: c for c in future}

        for coin in current:
            name = coin["name"]

            if name not in future_map:
                continue

            old_price = coin["price"]
            new_price = future_map[name]["price"]

            growth = ((new_price - old_price) / old_price) * 100

            if name not in performance:
                performance[name] = []

            performance[name].append(growth)

    return performance


def get_learning_boost(coin_name):
    perf = evaluate_past_performance()

    if coin_name not in perf:
        return 0

    avg = sum(perf[coin_name]) / len(perf[coin_name])

    # IA simple pero poderosa
    if avg > 5:
        return 2
    elif avg > 0:
        return 1
    elif avg < -5:
        return -2
    else:
        return 0