def generate_dashboard(coins):
    coins = sorted(coins, key=lambda x: x["score"], reverse=True)

    html = ""

    for c in coins:
        html += f"""
        <div class="coin">
            <b>{c['name']}</b> |
            ${c['price']:.2f} |
            {c['change']:.2f}% |
            <span>{c['tag']}</span> |
            Score: {c['score']}
        </div>
        """

    template = f"""
    <html>
    <head>
    <style>
    body {{
        background:black;
        color:#00ff99;
        font-family:monospace;
        text-align:center;
    }}
    .coin {{
        border-bottom:1px solid #222;
        padding:10px;
    }}
    </style>
    </head>
    <body>
    <h1>⛏️ DMR4 AI MINER</h1>
    {html}
    </body>
    </html>
    """

    with open("index.html", "w") as f:
        f.write(template)