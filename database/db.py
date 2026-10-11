import os
import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

try:
    import mysql.connector
except ImportError:  # pragma: no cover - optional dependency for MySQL mode
    mysql = None
else:
    mysql = __import__('mysql.connector')

BASE_DIR = Path(__file__).resolve().parent.parent


def db_connection():
    use_mysql = os.getenv("USE_MYSQL", "false").lower() == "true"
    if use_mysql:
        if mysql is None:
            raise RuntimeError("MySQL support is enabled, but mysql-connector-python is not installed.")
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "railway_system"),
            autocommit=True,
        )

    conn = sqlite3.connect(BASE_DIR / "railway.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    use_mysql = os.getenv("USE_MYSQL", "false").lower() == "true"
    schema_name = "schema.sql" if use_mysql else "schema_sqlite.sql"
    schema_sql = BASE_DIR / "database" / schema_name

    conn = db_connection()
    cur = conn.cursor()
    with open(schema_sql, "r", encoding="utf-8") as f:
        sql = f.read()
    for statement in sql.split(";"):
        line = statement.strip()
        if line:
            cur.execute(line)
    conn.commit()
    seed_sample_data()
    conn.close()


def seed_sample_data():
    conn = db_connection()
    cur = conn.cursor()
    seed_users = [
        ("Admin User", "admin@railway.com", "admin123", "admin"),
        ("Rahul Kumar", "rahul@example.com", "rahul123", "user"),
    ]
    for name, email, password, role in seed_users:
        cur.execute("SELECT 1 FROM users WHERE email = ? LIMIT 1", (email,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, generate_password_hash(password), role),
            )

    cur.execute("SELECT COUNT(*) FROM trains")
    train_count = cur.fetchone()[0]
    if train_count == 0:
        train_rows = [
            ("12001", "Bareilly Express", "Bareilly", "Delhi", "08:30:00", "11:15:00", "2h 45m", 420.00, 120, 76, "Sleeper"),
            ("12487", "Shatabdi Deluxe", "Delhi", "Agra", "09:00:00", "10:45:00", "1h 45m", 650.00, 90, 58, "AC"),
            ("12911", "Jaipur Queen", "Agra", "Jaipur", "14:20:00", "18:00:00", "3h 40m", 710.00, 110, 64, "AC"),
            ("14221", "Lucknow Mail", "Lucknow", "Kanpur", "07:15:00", "09:10:00", "1h 55m", 350.00, 100, 67, "Sleeper"),
            ("12345", "Northern Link", "Bareilly", "Lucknow", "18:50:00", "21:40:00", "2h 50m", 480.00, 130, 82, "Sleeper"),
            ("15012", "Rajasthan Wing", "Jaipur", "Jodhpur", "06:10:00", "10:20:00", "4h 10m", 780.00, 140, 92, "AC"),
            ("14707", "Punjab Star", "Chandigarh", "Delhi", "05:40:00", "08:00:00", "2h 20m", 590.00, 80, 49, "AC"),
            ("12389", "Northern Heritage", "Delhi", "Bareilly", "17:20:00", "19:50:00", "2h 30m", 460.00, 96, 61, "Sleeper"),
        ]
        cur.executemany(
            "INSERT INTO trains (train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats, available_seats, class_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            train_rows,
        )
    conn.commit()
    conn.close()
