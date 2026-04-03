import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(coin):
    if not BOT_TOKEN or not CHAT_ID:
        return

    message = (
        f"{coin['tag']}\n"
        f"{coin['name']}\n"
        f"💰 ${coin['price']:.4f}\n"
        f"📈 {coin['change']:.2f}%\n"
        f"🧠 {coin['prediction']}\n"
        f"⭐ Score: {coin['score']}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })
    except:
        pass