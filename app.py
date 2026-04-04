from flask import Flask, render_template, request, session, redirect
from database import init_db, get_db
from auth import login, register
from payments import create_checkout
import json, os

app = Flask(__name__)

# 🔐 CLAVE SEGURA
app.secret_key = os.getenv("SECRET_KEY", "fallback-key")

# 🔒 CONFIGURACIÓN SEGURA DE COOKIES
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # poner True en producción HTTPS
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

def get_user():
    if "user_id" not in session:
        return None
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

@app.route("/")
def index():
    coins = get_latest()
    user = get_user()

    if user and user["is_pro"] == 0:
        coins = [c for c in coins if c["score"] < 8]

    return render_template("index.html", coins=coins, user=user)

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
    user = get_user()
    if not user:
        return redirect("/login")

    db = get_db()
    db.execute(
        "UPDATE users SET is_pro=1 WHERE id=?",
        (user["id"],)
    )
    db.commit()

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()