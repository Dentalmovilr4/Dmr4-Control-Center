from flask import Flask, render_template, request, session, redirect
import json, os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dmr4-secret")

FILE = "data/history.json"

# ================= SAFE IMPORTS =================

try:
    from database import init_db, get_db
    init_db()
    DB_OK = True
except:
    DB_OK = False

try:
    from auth import login, register
except:
    def login(): return "login disabled"
    def register(): return "register disabled"

try:
    from payments import create_checkout, activate_plan
except:
    def create_checkout(plan): return f"payments disabled: {plan}"
    def activate_plan(user, plan): pass

try:
    from plans import filter_coins_by_plan
except:
    def filter_coins_by_plan(coins, plan): return coins


# ================= DATA =================

def get_latest():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            history = json.load(f)
        if not history:
            return []
        return history[-1]["coins"]
    except:
        return []


def get_user():
    if not DB_OK:
        return None

    if "user_id" not in session:
        return None

    try:
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
    except:
        return None


# ================= ROUTES =================

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

    if "user_id" in session:
        activate_plan(session["user_id"], plan)

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= START =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)