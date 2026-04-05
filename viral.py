import os
import requests
import random
import google.generativeai as genai

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Nueva clave de Google
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuración de la IA de Google
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def get_ai_opinion(coin_name, change, score):
    """Genera un análisis estricto y profesional con Gemini"""
    if not model:
        return "Análisis técnico en proceso..."
    
    try:
        prompt = (
            f"Analiza la criptomoneda {coin_name} con un cambio de {change}% y un score de {score}/100. "
            "Da una opinión técnica muy breve (máximo 15 palabras) para inversores exigentes. "
            "Sé estricto y profesional."
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Evaluando métricas de mercado..."

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
    
    # Generamos el análisis inteligente de Google
    opinion_ia = get_ai_opinion(top['name'], top['change'], top['score'])

    message = f"""
{hook}

🪙 {top['name']}
💰 Precio: ${top['price']:.4f}
📈 Cambio: {top['change']:.2f}%
🧠 Score: {top['score']}

🤖 IA ANALYST: {opinion_ia}
⚠️ ESTADO: {top['prediction']}

👉 Mira más señales:
https://dmr4-control-center.onrender.com
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
