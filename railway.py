import os
import random
from datetime import datetime, date

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from database.db import db_connection, init_db
from dsa.graph import RailwayGraph
from dsa.hash_table import HashTable
from dsa.queue import RailwayQueue
from dsa.sorting import sort_trains
from dsa.stack import RailwayStack
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.routes import routes_bp
from routes.trains import trains_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(trains_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(routes_bp)

    app.config["WAITING_QUEUE"] = {}
    app.config["CANCELLATION_STACK"] = RailwayStack()
    app.config["PNR_HASH"] = HashTable()

    @app.context_processor
    def inject_user():
        return {
            "current_user": session.get("user"),
            "is_admin": session.get("user", {}).get("role") == "admin" if isinstance(session.get("user"), dict) else False,
        }

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        if not session.get("user"):
            return redirect(url_for("auth.login"))
        return render_template("admin/dashboard.html")

    @app.route("/api/register", methods=["POST"])
    def api_register():
        payload = request.get_json(silent=True) or request.form
        name = (payload.get("name") or "").strip()
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password") or ""
        if not name or not email or not password:
            return jsonify({"success": False, "message": "All fields are required."}), 400
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            conn.close()
            return jsonify({"success": False, "message": "Email already exists."}), 409
        hashed = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'user')",
            (name, email, hashed),
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Registration successful."})

    @app.route("/api/login", methods=["POST"])
    def api_login():
        payload = request.get_json(silent=True) or request.form
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password") or ""
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required."}), 400
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if not user:
            conn.close()
            return jsonify({"success": False, "message": "Invalid credentials."}), 401
        if not check_password_hash(user["password"], password):
            conn.close()
            return jsonify({"success": False, "message": "Invalid credentials."}), 401
        session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}
        conn.close()
        return jsonify({"success": True, "user": session["user"]})

    @app.route("/api/logout", methods=["POST"])
    def api_logout():
        session.pop("user", None)
        return jsonify({"success": True, "message": "Logged out successfully."})

    @app.route("/api/trains")
    def api_trains():
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM trains ORDER BY departure_time")
        rows = cur.fetchall()
        conn.close()
        return jsonify({"success": True, "trains": [dict(r) for r in rows]})

    @app.route("/api/trains/search")
    def api_trains_search():
        source = request.args.get("source", "").strip()
        destination = request.args.get("destination", "").strip()
        sort_by = request.args.get("sort_by", "departure_time")
        conn = db_connection()
        cur = conn.cursor()
        query = "SELECT * FROM trains WHERE source LIKE ? AND destination LIKE ?"
        params = [f"%{source}%", f"%{destination}%"]
        if source and destination:
            cur.execute(query, params)
        else:
            cur.execute("SELECT * FROM trains")
        rows = cur.fetchall()
        train_list = [dict(r) for r in rows]
        sorted_rows = sort_trains(train_list, sort_by)
        conn.close()
        return jsonify({"success": True, "trains": sorted_rows})

    @app.route("/api/book", methods=["POST"])
    def api_book():
        payload = request.get_json(silent=True) or request.form
        if not session.get("user"):
            return jsonify({"success": False, "message": "Please log in."}), 401
        train_id = payload.get("train_id")
        passenger_name = (payload.get("passenger_name") or "").strip()
        age = int(payload.get("age") or 0)
        gender = (payload.get("gender") or "").strip()
        journey_date = payload.get("journey_date")
        travel_class = payload.get("class_name") or payload.get("class")
        if not all([train_id, passenger_name, age, gender, journey_date, travel_class]):
            return jsonify({"success": False, "message": "Please provide all booking details."}), 400
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM trains WHERE id = ?", (train_id,))
        train = cur.fetchone()
        if not train:
            conn.close()
            return jsonify({"success": False, "message": "Train not found."}), 404
        if train["available_seats"] <= 0:
            queue = app.config["WAITING_QUEUE"].get(str(train_id), RailwayQueue())
            queue.enqueue({
                "passenger_name": passenger_name,
                "age": age,
                "gender": gender,
                "journey_date": journey_date,
                "class": travel_class,
                "user_id": session["user"]["id"],
            })
            app.config["WAITING_QUEUE"][str(train_id)] = queue
            pnr = str(random.randint(1000000000, 9999999999))
            cur.execute(
                "INSERT INTO waiting_list (booking_id, train_id, passenger_name, pnr, position, status) VALUES (NULL, ?, ?, ?, ?, 'WAITING')",
                (train_id, passenger_name, pnr, queue.size()),
            )
            conn.commit()
            conn.close()
            return jsonify({"success": True, "waiting": True, "message": "No confirmed seats available. Added to waiting list.", "pnr": pnr})
        pnr = str(random.randint(1000000000, 9999999999))
        seat_number = f"{train['train_number']}-{random.randint(1, 100)}"
        cur.execute(
            "INSERT INTO bookings (pnr, user_id, train_id, passenger_name, age, gender, journey_date, class, seat_number, status, booking_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'CONFIRMED', datetime('now'))",
            (pnr, session["user"]["id"], train_id, passenger_name, age, gender, journey_date, travel_class, seat_number),
        )
        cur.execute("UPDATE trains SET available_seats = available_seats - 1 WHERE id = ?", (train_id,))
        conn.commit()
        conn.close()
        app.config["PNR_HASH"].set(pnr, {"passenger_name": passenger_name, "pnr": pnr, "train_id": train_id})
        return jsonify({"success": True, "waiting": False, "pnr": pnr, "seat_number": seat_number, "train": dict(train)})

    @app.route("/api/bookings")
    def api_bookings():
        if not session.get("user"):
            return jsonify({"success": False, "message": "Unauthorized"}), 401
        user_id = session["user"]["id"]
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT b.*, t.train_number, t.train_name, t.source, t.destination, t.departure_time, t.arrival_time FROM bookings b JOIN trains t ON t.id = b.train_id WHERE b.user_id = ? ORDER BY b.booking_time DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        conn.close()
        return jsonify({"success": True, "bookings": [dict(row) for row in rows]})

    @app.route("/api/pnr/<pnr>")
    def api_pnr_lookup(pnr):
        data = app.config["PNR_HASH"].get(pnr)
        if data:
            return jsonify({"success": True, "booking": data})
        return jsonify({"success": False, "message": "PNR not found."}), 404

    @app.route("/api/cancel/<pnr>", methods=["POST"])
    def api_cancel(pnr):
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM bookings WHERE pnr = ?", (pnr,))
        booking = cur.fetchone()
        if not booking:
            conn.close()
            return jsonify({"success": False, "message": "Booking not found."}), 404
        cur.execute("UPDATE bookings SET status = 'CANCELLED' WHERE pnr = ?", (pnr,))
        cur.execute("UPDATE trains SET available_seats = available_seats + 1 WHERE id = ?", (booking["train_id"],))
        cur.execute("INSERT INTO cancellations (pnr, cancellation_time, refund_amount, status) VALUES (?, datetime('now'), 0, 'CANCELLED')", (pnr,))
        app.config["CANCELLATION_STACK"].push({"pnr": pnr, "passenger_name": booking["passenger_name"]})
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Ticket cancelled successfully.", "pnr": pnr})

    app.config["GRAPH"] = RailwayGraph()
    station_connections = [
        ("Bareilly", "Delhi"), ("Delhi", "Agra"), ("Agra", "Jaipur"), ("Delhi", "Lucknow"),
        ("Lucknow", "Kanpur"), ("Jaipur", "Jodhpur"), ("Bareilly", "Lucknow"), ("Chandigarh", "Delhi")
    ]
    for source, destination in station_connections:
        app.config["GRAPH"].add_edge(source, destination)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
