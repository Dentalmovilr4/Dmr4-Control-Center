def analyze_coin(coin):
    quote = coin["quote"]["USD"]

    price = quote["price"]
    change = quote["percent_change_24h"]
    volume = quote["volume_24h"]
    market_cap = quote["market_cap"]

    score = 0

    # 🔥 lógica inteligente
    if change > 5:
        score += 3
    if volume > 1_000_000:
        score += 2
    if market_cap < 500_000_000:
        score += 3
    if change > 10:
        score += 5

    # clasificación
    if score >= 8:
        tag = "💎 GEMA"
    elif score >= 5:
        tag = "⛏️ MINA"
    else:
        tag = "🪨 NORMAL"

    return {
        "name": coin["name"],
        "price": price,
        "change": change,
        "volume": volume,
        "score": score,
        "tag": tag
    }