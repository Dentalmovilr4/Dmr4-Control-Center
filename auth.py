from flask import request, redirect, session
from database import get_db
import bcrypt

def register():
    username = request.form["username"]
    password = request.form["password"]

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s,%s)",
            (username, hashed)
        )
        conn.commit()
    except:
        return "Usuario ya existe"

    cur.close()
    conn.close()

    return redirect("/login")

def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE username=%s",
        (username,)
    )
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        session["user_id"] = user[0]
        return redirect("/")

    return "Login incorrecto"