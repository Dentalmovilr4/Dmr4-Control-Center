from flask import Flask, render_template, request, session, redirect
from database import init_db, get_db
from auth import login, register
from payments import create_checkout
import json, os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

init_db()

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

    if "user_id" not in session:
        return render_template("index.html", coins=[])

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT is_pro FROM users WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and user[0] == 0:
        coins = [c for c in coins if c["score"] < 8]

    return render_template("index.html", coins=coins)

@app.route("/login", methods=["GET","POST"])
def login_route():
    if request.method == "POST":
        return login()
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register_route():
    if request.method == "POST":
        return register()
    return render_template("register.html")

@app.route("/pay")
def pay():
    return create_checkout()

@app.route("/success")
def success():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET is_pro=1 WHERE id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()