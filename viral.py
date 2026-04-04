import os
import requests
import random

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def build_message(coins):
    if not coins:
        return None

    top = coins[0]

    hooks = [
        "🚨 ALERTA TEMPRANA DETECTADA",
        "🔥 POSIBLE GEM ANTES DE EXPLOTAR",
        "📡 SEÑAL FILTRADA POR IA",
        "💎 OPORTUNIDAD DETECTADA"
    ]

    hook = random.choice(hooks)

    message = f"""
{hook}

🪙 {top['name']}
💰 Precio: ${top['price']:.4f}
📈 Cambio: {top['change']:.2f}%
🧠 Score: {top['score']}

🤖 IA: {top['prediction']}

👉 Mira más señales:
https://TU-APP.onrender.com
"""

    return message

def send_viral(coins):
    message = build_message(coins)

    if not message:
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })