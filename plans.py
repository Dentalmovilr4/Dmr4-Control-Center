def filter_coins_by_plan(coins, plan):
    if plan == "free":
        return [c for c in coins if c["score"] < 6]

    elif plan == "pro":
        return [c for c in coins if c["score"] < 10]

    elif plan == "elite":
        return coins

    return []