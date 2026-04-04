from flask import request, redirect, session
from database import get_db
import bcrypt

def register():
    username = request.form["username"]
    password = request.form["password"]

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?,?)",
            (username, hashed)
        )
        db.commit()
    except:
        return "Usuario ya existe"

    return redirect("/login")

def login():
    username = request.form["username"]
    password = request.form["password"]

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if user and bcrypt.checkpw(password.encode(), user["password"]):
        session["user_id"] = user["id"]
        return redirect("/")

    return "Login incorrecto"