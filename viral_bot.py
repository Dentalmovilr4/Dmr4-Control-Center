import os
import requests
from storage import load_history

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_top_signal():
    history = load_history()
    if not history:
        return None

    coins = history[-1]["coins"]
    coins = sorted(coins, key=lambda x: x["score"], reverse=True)

    return coins[0] if coins else None

def format_message(c):
    return f"""
🚀 DMR4 SIGNAL

💰 {c['name']}
📈 {c['change']:.2f}%
🧠 Score: {c['score']}
🤖 {c['prediction']}

#crypto #bitcoin #trading
"""

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

def post_twitter(msg):
    # Placeholder (puedes conectar API luego)
    print("POST TWITTER:", msg)

def run():
    coin = get_top_signal()

    if not coin:
        return

    if coin["score"] < 10:
        return  # solo señales fuertes

    msg = format_message(coin)

    send_telegram(msg)
    post_twitter(msg)

if __name__ == "__main__":
    run()