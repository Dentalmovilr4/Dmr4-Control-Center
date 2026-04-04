import os
import json
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier

FILE = "data/history.json"
MODEL_FILE = "data/institutional_model.pkl"

def load_history():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

# ================= FEATURES AVANZADAS =================

def compute_features(coin):
    change = coin["change"]
    score = coin["score"]

    # features derivadas tipo institucional
    momentum = change
    volatility = abs(change)
    strength = score

    return [momentum, volatility, strength]

# ================= DATASET =================

def build_dataset():
    history = load_history()

    X = []
    y = []

    if len(history) < 2:
        return None, None

    for i in range(len(history) - 1):
        current = history[i]["coins"]
        future = history[i + 1]["coins"]

        future_map = {c["name"]: c for c in future}

        for coin in current:
            name = coin["name"]

            if name not in future_map:
                continue

            old_price = coin["price"]
            new_price = future_map[name]["price"]

            growth = (new_price - old_price) / old_price

            features = compute_features(coin)

            label = 1 if growth > 0.05 else 0

            X.append(features)
            y.append(label)

    if not X:
        return None, None

    return np.array(X), np.array(y)

# ================= ENTRENAMIENTO =================

def train_model():
    X, y = build_dataset()

    if X is None:
        return None

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    os.makedirs("data", exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    return model

def load_model():
    if not os.path.exists(MODEL_FILE):
        return train_model()

    return joblib.load(MODEL_FILE)

# ================= PREDICCIÓN =================

def predict_coin(coin):
    model = load_model()

    if not model:
        return 0.5

    features = np.array([compute_features(coin)])

    prob = model.predict_proba(features)[0][1]

    return prob