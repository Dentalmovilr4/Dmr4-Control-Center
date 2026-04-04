from ai_institutional import predict_coin

def analyze_coin(coin, history):
    try:
        name = coin["name"]
        price = coin["quote"]["USD"]["price"]
        change = coin["quote"]["USD"]["percent_change_24h"]
        volume = coin["quote"]["USD"]["volume_24h"]

        score = 0

        if change > 5:
            score += 5
        if volume > 1_000_000:
            score += 3
        if change > 20:
            score += 5

        prob = predict_coin({
            "change": change,
            "score": score
        })

        if prob > 0.7:
            score += 5

        if prob > 0.85:
            tag = "🔥 STRONG BUY"
            prediction = "entrada institucional"
        elif prob > 0.65:
            tag = "📈 BUY"
            prediction = "probabilidad positiva"
        elif prob > 0.5:
            tag = "⚖️ HOLD"
            prediction = "esperar"
        else:
            tag = "❌ AVOID"
            prediction = "riesgo alto"

        return {
            "name": name,
            "price": price,
            "change": change,
            "score": score,
            "probability": prob,
            "tag": tag,
            "prediction": prediction
        }

    except:
        return None