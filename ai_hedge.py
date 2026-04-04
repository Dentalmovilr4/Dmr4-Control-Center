import os
import json
import numpy as np
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

FILE = "data/history.json"
MODEL_DIR = "data/models"

def load_history():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

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

            features = [
                coin["change"],
                coin["score"]
            ]

            label = 1 if growth > 0.05 else 0

            X.append(features)
            y.append(label)

    if not X:
        return None, None

    return np.array(X), np.array(y)

def train_models():
    X, y = build_dataset()

    if X is None:
        return None

    os.makedirs(MODEL_DIR, exist_ok=True)

    # Modelo 1
    lr = LogisticRegression()
    lr.fit(X, y)
    joblib.dump(lr, f"{MODEL_DIR}/lr.pkl")

    # Modelo 2
    rf = RandomForestClassifier(n_estimators=50)
    rf.fit(X, y)
    joblib.dump(rf, f"{MODEL_DIR}/rf.pkl")

def load_models():
    models = []

    try:
        models.append(joblib.load(f"{MODEL_DIR}/lr.pkl"))
        models.append(joblib.load(f"{MODEL_DIR}/rf.pkl"))
    except:
        return None

    return models

def predict_ensemble(change, score):
    models = load_models()

    if not models:
        return 0.5

    features = np.array([[change, score]])

    probs = []

    for model in models:
        try:
            p = model.predict_proba(features)[0][1]
            probs.append(p)
        except:
            continue

    if not probs:
        return 0.5

    # 🧠 promedio tipo hedge fund
    return sum(probs) / len(probs)