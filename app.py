from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB_PATH = Path("weather.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            condition TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return """
    <html>
      <head>
        <title>Weather Tracker App</title>
      </head>
      <body>
        <h1>Weather Tracker App</h1>
        <p>This Flask app stores weather observations in SQLite.</p>
        <p>Available endpoints:</p>
        <ul>
          <li>GET /health</li>
          <li>GET /weather</li>
          <li>GET /weather/&lt;city&gt;</li>
          <li>POST /weather</li>
        </ul>
      </body>
    </html>
    """


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/weather", methods=["GET"])
def get_weather():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, city, timestamp, temperature, condition FROM weather ORDER BY id ASC"
    ).fetchall()
    conn.close()

    weather_data = [dict(row) for row in rows]
    return jsonify(weather_data), 200


@app.route("/weather/<city>", methods=["GET"])
def get_weather_by_city(city):
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT id, city, timestamp, temperature, condition
        FROM weather
        WHERE LOWER(city) = LOWER(?)
        ORDER BY id ASC
        """,
        (city,),
    ).fetchall()
    conn.close()

    weather_data = [dict(row) for row in rows]
    return jsonify(weather_data), 200


@app.route("/weather", methods=["POST"])
def add_weather():
    data = request.get_json(silent=True)

    required_fields = {"city", "timestamp", "temperature", "condition"}
    if not data or not required_fields.issubset(data.keys()):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO weather (city, timestamp, temperature, condition)
        VALUES (?, ?, ?, ?)
        """,
        (
            data["city"],
            data["timestamp"],
            data["temperature"],
            data["condition"],
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return (
        jsonify(
            {
                "id": new_id,
                "city": data["city"],
                "timestamp": data["timestamp"],
                "temperature": data["temperature"],
                "condition": data["condition"],
            }
        ),
        201,
    )


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
