import json
import os
from datetime import datetime

JSON_FILE = "data/history.json"
DATABASE_URL = os.getenv("DATABASE_URL")

USE_DB = False

# validar si es una URL válida de postgres
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    try:
        import psycopg2
        USE_DB = True
    except:
        USE_DB = False


def load_history():
    # intentar DB
    if USE_DB:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()

            cur.execute("SELECT data FROM history ORDER BY id DESC LIMIT 50")
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return [r[0] for r in reversed(rows)]
        except:
            pass

    # fallback JSON
    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r") as f:
        return json.load(f)


def save_snapshot(results):
    snapshot = {
        "timestamp": str(datetime.now()),
        "coins": results
    }

    # intentar DB
    if USE_DB:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id SERIAL PRIMARY KEY,
                timestamp TEXT,
                data JSONB
            )
            """)

            cur.execute(
                "INSERT INTO history (timestamp, data) VALUES (%s, %s)",
                (snapshot["timestamp"], json.dumps(snapshot))
            )

            conn.commit()
            cur.close()
            conn.close()
            return
        except:
            pass

    # fallback JSON
    history = load_history()
    history.append(snapshot)

    os.makedirs("data", exist_ok=True)

    with open(JSON_FILE, "w") as f:
        json.dump(history[-50:], f, indent=2)