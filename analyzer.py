def analyze_coin(coin, history):
    quote = coin["quote"]["USD"]

    name = coin["name"]
    price = quote["price"]
    change = quote["percent_change_24h"]
    volume = quote["volume_24h"]
    market_cap = quote["market_cap"]

    # 🚫 filtro basura
    if change > 50 or volume < 500000:
        return None

    score = 0

    # 📡 base radar
    if 2 < change < 10:
        score += 3

    if volume > 2_000_000:
        score += 3

    if market_cap < 300_000_000:
        score += 3

    # 🧠 IA: tendencia histórica
    trend_score = 0

    coin_history = []
    for snapshot in history[-10:]:
        for c in snapshot["coins"]:
            if c["name"] == name:
                coin_history.append(c)

    if len(coin_history) >= 3:
        increases = 0

        for c in coin_history:
            if c["change"] > 0:
                increases += 1

        if increases >= 3:
            trend_score += 4  # tendencia positiva

    # 📈 IA: volumen creciente
    if len(coin_history) >= 3:
        vols = [c["volume"] for c in coin_history[-3:]]

        if vols[2] > vols[1] > vols[0]:
            trend_score += 4  # acumulación real

    total_score = score + trend_score

    # 🔮 predicción
    if total_score >= 10:
        prediction = "🚀 EXPLOSIÓN INMINENTE"
        tag = "🔥 ALTA PROBABILIDAD"
    elif total_score >= 7:
        prediction = "📈 SUBIDA PROBABLE"
        tag = "📡 RADAR"
    elif total_score >= 5:
        prediction = "👀 CRECIMIENTO LENTO"
        tag = "👀 OBSERVAR"
    else:
        return None

    return {
        "name": name,
        "price": price,
        "change": change,
        "volume": volume,
        "market_cap": market_cap,
        "score": total_score,
        "prediction": prediction,
        "tag": tag
    }