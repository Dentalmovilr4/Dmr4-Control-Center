from flask import Flask, render_template
import json
import os

app = Flask(__name__)

FILE = "data/history.json"

def get_latest():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        history = json.load(f)

    if not history:
        return []

    return history[-1]["coins"]

@app.route("/")
def index():
    coins = get_latest()
    coins = sorted(coins, key=lambda x: x["score"], reverse=True)
    return render_template("index.html", coins=coins)

if __name__ == "__main__":
    app.run()