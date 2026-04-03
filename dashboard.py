def generate_dashboard(coins):
    coins = sorted(coins, key=lambda x: x["score"], reverse=True)

    html = ""

    for c in coins:
        html += f"""
        <div class="coin">
            <b>{c['name']}</b> |
            ${c['price']:.4f} |
            {c['change']:.2f}% |
            {c['tag']} |
            🤖 {c['prediction']} |
            ⭐ {c['score']}
        </div>
        """

    template = f"""
    <html>
    <body style="background:black;color:#00ff99;font-family:monospace;text-align:center">
    <h1>🧠 DMR4 IA EXPERTA</h1>
    {html}
    </body>
    </html>
    """

    with open("index.html", "w") as f:
        f.write(template)