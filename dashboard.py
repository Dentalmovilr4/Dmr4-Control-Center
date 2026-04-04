import json
from storage import load_history

def generate_dashboard(coins):
    coins = sorted(coins, key=lambda x: x["score"], reverse=True)

    # 🧠 obtener histórico
    history = load_history()

    chart_data = {}

    for snapshot in history[-10:]:  # últimas 10 ejecuciones
        for coin in snapshot["coins"]:
            name = coin["name"]
            if name not in chart_data:
                chart_data[name] = []

            chart_data[name].append(coin["change"])

    coins_html = ""
    charts_html = ""

    for c in coins[:5]:  # solo top 5 para gráficas
        name = c["name"]

        coins_html += f"""
        <div class="coin">
            <b>{name}</b> |
            ${c['price']:.4f} |
            {c['change']:.2f}% |
            {c['tag']} |
            🤖 {c['prediction']}
        </div>
        """

        data = chart_data.get(name, [])

        charts_html += f"""
        <h3>{name}</h3>
        <canvas id="chart_{name.replace(' ', '')}"></canvas>
        <script>
        new Chart(document.getElementById("chart_{name.replace(' ', '')}"), {{
            type: 'line',
            data: {{
                labels: {list(range(len(data)))},
                datasets: [{{
                    label: '{name}',
                    data: {data},
                    fill: false
                }}]
            }}
        }});
        </script>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>

    <body style="background:black;color:#00ff99;font-family:monospace;text-align:center">

    <h1>📊 DMR4 AI RADAR</h1>

    {coins_html}

    <h2>📈 Tendencia en tiempo real</h2>

    {charts_html}

    </body>
    </html>
    """

    with open("index.html", "w") as f:
        f.write(html)