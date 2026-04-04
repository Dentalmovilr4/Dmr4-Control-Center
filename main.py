from miner import get_market_data
from analyzer import analyze_coin
from storage import save_snapshot, load_history
from viral import send_viral
from ai_institutional import train_model
from fund_manager import simulate_trades

def run():
    raw = get_market_data()
    history = load_history()

    results = []

    for coin in raw:
        try:
            result = analyze_coin(coin, history)

            if result:
                results.append(result)

        except:
            continue

    save_snapshot(results)

    # 🧠 entrenar IA
    train_model()

    # 💰 simular fondo
    fund = simulate_trades()

    print(f"💰 Capital actual: ${fund['capital']:.2f}")

    if results:
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        send_viral(results)

if __name__ == "__main__":
    run()