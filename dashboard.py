import json
from storage import load_history

def generate_dashboard(coins):
    coins = sorted(coins, key=lambda x: x["score"], reverse=True)
    history = load_history()

    # 📊 métricas generales
    total = len(coins)
    strong = len([c for c in coins if c["score"] >= 10])
    radar = len([c for c in coins if 7 <= c["score"] < 10])

    # 📡 lista de monedas
    coins_html = ""
    charts_html = ""

    for c in coins[:10]:
        name = c["name"]
        safe_name = name.replace(" ", "").replace(".", "").replace("-", "")

        coins_html += f"""
        <tr>
            <td>{name}</td>
            <td>${c['price']:.4f}</td>
            <td>{c['change']:.2f}%</td>
            <td>{c['score']}</td>
            <td>{c['tag']}</td>
            <td>{c['prediction']}</td>
        </tr>
        """

        # 📈 datos históricos
        data = []

        for snapshot in history[-10:]:
            for coin in snapshot["coins"]:
                if coin["name"] == name:
                    data.append(coin["change"])

        charts_html += f"""
        <div class="chart-box">
            <h3>{name}</h3>
            <canvas id="chart_{safe_name}"></canvas>
            <script>
            new Chart(document.getElementById("chart_{safe_name}"), {{
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
        </div>
        """

    # 🌐 HTML PRO
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>DMR4 PRO PANEL</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {{
    background:#050505;
    color:#00ff99;
    font-family: monospace;
    margin:0;
}}

/* HEADER */
.header {{
    padding:20px;
    text-align:center;
    border-bottom:1px solid #111;
}}

h1 {{
    color:#00e5ff;
}}

/* STATS */
.stats {{
    display:flex;
    justify-content:space-around;
    padding:20px;
}}

.card {{
    border:1px solid #00ff99;
    padding:15px;
    width:30%;
    box-shadow:0 0 10px #00ff99;
}}

/* TABLA */
table {{
    width:90%;
    margin:auto;
    border-collapse: collapse;
}}

th, td {{
    padding:10px;
    border-bottom:1px solid #222;
}}

tr:hover {{
    background:#111;
}}

/* GRÁFICAS */
.charts {{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
}}

.chart-box {{
    width:300px;
    margin:20px;
    border:1px solid #222;
    padding:10px;
}}
</style>

</head>

<body>

<div class="header">
    <h1>🧠 DMR4 AI PRO PANEL</h1>
    <p>Sistema de detección inteligente en tiempo real</p>
</div>

<div class="stats">
    <div class="card">Total activos: {total}</div>
    <div class="card">🔥 Alta probabilidad: {strong}</div>
    <div class="card">📡 En radar: {radar}</div>
</div>

<h2 style="text-align:center;">📊 Ranking de oportunidades</h2>

<table>
<tr>
<th>Moneda</th>
<th>Precio</th>
<th>%</th>
<th>Score</th>
<th>Señal</th>
<th>IA</th>
</tr>

{coins_html}

</table>

<h2 style="text-align:center;">📈 Análisis de tendencia</h2>

<div class="charts">
{charts_html}
</div>

</body>
</html>
"""

    with open("index.html", "w") as f:
        f.write(html)