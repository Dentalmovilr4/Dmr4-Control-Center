import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('CMC_API_KEY')

def generate_dashboard(coins_html):
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dmr4 Control Center - AI Scout</title>
        <style>
            body {{ background-color: #0a0a0a; color: #00ff99; font-family: monospace; text-align: center; }}
            .container {{ margin-top: 50px; border: 2px solid #00ff99; display: inline-block; padding: 20px; box-shadow: 0 0 15px #00ff99; }}
            .coin {{ border-bottom: 1px solid #333; padding: 10px; }}
            .high-potential {{ color: #ff00ff; text-shadow: 0 0 5px #ff00ff; }}
            h1 {{ color: #00e5ff; text-shadow: 0 0 10px #00e5ff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DMR4 AI MONITOR</h1>
            {coins_html}
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("✅ Dashboard 'index.html' generado con éxito.")

def scout_profitable_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    # CORRECCIÓN AQUÍ: Quitamos las llaves dobles
    parameters = {
        'start': '1', 
        'limit': '10', 
        'convert': 'USD', 
        'sort': 'percent_change_24h'
    }
    headers = {
        'Accepts': 'application/json', 
        'X-CMC_PRO_API_KEY': API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        coins_html = ""
        
        print("--- [Dmr4 AI Scouting Report] ---")
        for coin in data['data']:
            name = coin['name']
            price = coin['quote']['USD']['price']
            change = coin['quote']['USD']['percent_change_24h']
            
            status = "🚀 ALTO POTENCIAL" if change > 5 else "⚖️ ESTABLE"
            class_name = "high-potential" if change > 5 else ""
            
            print(f"Moneda: {name} | Cambio: {change:.2f}% | {status}")
            coins_html += f'<div class="coin"><b>{name}</b>: ${price:.2f} | <span class="{class_name}">{change:.2f}%</span></div>'
        
        generate_dashboard(coins_html)
            
    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    scout_profitable_coins()

