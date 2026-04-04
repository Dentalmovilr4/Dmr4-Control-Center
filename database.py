import psycopg2
import os

def get_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        is_pro INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    cur.close()
    conn.close()