from flask import request, redirect, session
from database import get_db

def register():
    username = request.form["username"]
    password = request.form["password"]

    db = get_db()
    db.execute("INSERT INTO users (username, password) VALUES (?,?)",
               (username, password))
    db.commit()

    return redirect("/login")

def login():
    username = request.form["username"]
    password = request.form["password"]

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    if user:
        session["user_id"] = user["id"]
        return redirect("/")
    
    return "Login incorrecto"