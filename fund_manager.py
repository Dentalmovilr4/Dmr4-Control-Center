import json
import os

FILE = "data/history.json"
FUND_FILE = "data/fund.json"

INITIAL_CAPITAL = 1000  # capital inicial

def load_history():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def load_fund():
    if not os.path.exists(FUND_FILE):
        return {
            "capital": INITIAL_CAPITAL,
            "positions": []
        }
    with open(FUND_FILE, "r") as f:
        return json.load(f)

def save_fund(fund):
    os.makedirs("data", exist_ok=True)
    with open(FUND_FILE, "w") as f:
        json.dump(fund, f, indent=2)

def simulate_trades():
    history = load_history()
    fund = load_fund()

    if len(history) < 2:
        return fund

    latest = history[-1]["coins"]
    previous = history[-2]["coins"]

    prev_map = {c["name"]: c for c in previous}

    for coin in latest:
        name = coin["name"]

        if name not in prev_map:
            continue

        prev_price = prev_map[name]["price"]
        current_price = coin["price"]

        growth = (current_price - prev_price) / prev_price

        # estrategia institucional simple
        if coin["probability"] > 0.7 and fund["capital"] > 10:
            investment = fund["capital"] * 0.1  # 10% capital

            profit = investment * growth

            fund["capital"] += profit

            fund["positions"].append({
                "coin": name,
                "investment": investment,
                "profit": profit
            })

    save_fund(fund)

    return fund