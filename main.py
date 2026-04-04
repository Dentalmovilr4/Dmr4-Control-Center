from miner import get_market_data
from analyzer import analyze_coin
from storage import save_snapshot, load_history
from notifier import send_alert

def run():
    raw = get_market_data()
    history = load_history()

    results = []

    for coin in raw:
        try:
            result = analyze_coin(coin, history)

            if not result:
                continue

            if result["score"] >= 10:
                send_alert(result)

            results.append(result)

        except:
            continue

    save_snapshot(results)

if __name__ == "__main__":
    run()
