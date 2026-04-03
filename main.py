from miner import get_market_data
from analyzer import analyze_coin
from storage import save_snapshot
from dashboard import generate_dashboard

def run():
    raw_data = get_market_data()

    analyzed = []

    for coin in raw_data:
        try:
            analyzed.append(analyze_coin(coin))
        except:
            continue

    save_snapshot(analyzed)
    generate_dashboard(analyzed)

if __name__ == "__main__":
    run()

