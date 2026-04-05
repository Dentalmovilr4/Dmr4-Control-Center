import json
import os
from datetime import datetime
from notifier import send_alert  # Importamos tu función de Telegram

# Configuración de rutas
DATA_DIR = "data"
FUND_FILE = os.path.join(DATA_DIR, "fund.json")
HIST_FILE = os.path.join(DATA_DIR, "history.json")

def inicializar_archivos():
    """Asegura que la carpeta y archivos existan para que Render no de error"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(FUND_FILE):
        with open(FUND_FILE, "w") as f:
            json.dump({"capital": 1000, "positions": []}, f, indent=4)
            
    if not os.path.exists(HIST_FILE):
        with open(HIST_FILE, "w") as f:
            json.dump([], f, indent=4)

def procesar_trading(market_data):
    inicializar_archivos()
    
    try:
        with open(FUND_FILE, "r") as f:
            cartera = json.load(f)
    except:
        return # Si el archivo está corrupto, mejor no hacer nada

    alertas_enviadas = 0

    for coin in market_data:
        symbol = coin.get('symbol')
        price = coin.get('quote', {}).get('USD', {}).get('price', 0)
        change_24h = coin.get('quote', {}).get('USD', {}).get('percent_change_24h', 0)

        # --- LÓGICA DE IA DMR4 ---
        # Si la moneda subió más de 5% en 24h, le damos un Score alto
        score = 50 + (change_24h * 2)
        score = max(0, min(100, score)) # Mantener entre 0 y 100

        if score > 85:
            # Preparamos el mensaje para Telegram
            mensaje = {
                "tag": "🔥 OPORTUNIDAD DETECTADA",
                "name": coin.get('name', symbol),
                "price": price,
                "change": change_24h,
                "prediction": "BULLISH 🚀",
                "score": round(score, 2)
            }
            
            # Solo mandamos alerta, no compramos todavía para no pelear con el JSON de Render
            send_alert(mensaje)
            alertas_enviadas += 1
            print(f"✅ Alerta enviada para {symbol} (Score: {score})")

    return f"Proceso terminado. Alertas sent: {alertas_enviadas}"
