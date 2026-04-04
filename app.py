from flask import Flask, render_template, request, session, redirect
from database import init_db, get_db
from auth import login, register
from payments import create_checkout, activate_plan
from plans import filter_coins_by_plan
import json, os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

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

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, plan FROM users WHERE id=%s",
        (session["user_id"],)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

@app.route("/")
def index():
    coins = get_latest()
    user = get_user()

    plan = "free"
    if user:
        plan = user[1]

    coins = filter_coins_by_plan(coins, plan)

    return render_template("index.html", coins=coins, plan=plan)

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

@app.route("/pay/<plan>")
def pay(plan):
    return create_checkout(plan)

@app.route("/success")
def success():
    plan = request.args.get("plan")
    activate_plan(session["user_id"], plan)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()