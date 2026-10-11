from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify

from database.db import db_connection

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
def ensure_admin():
    user = session.get("user")
    if request.path.startswith("/admin") and user and user.get("role") != "admin":
        return redirect(url_for("auth.login"))
    if request.path.startswith("/admin") and not user:
        return redirect(url_for("auth.admin_login"))


@admin_bp.route("/admin")
def admin_home():
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/admin/dashboard")
def dashboard():
    if not session.get("user") or session["user"].get("role") != "admin":
        return redirect(url_for("auth.admin_login"))
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cur.fetchone()["total_users"]
    cur.execute("SELECT COUNT(*) AS total_trains FROM trains")
    total_trains = cur.fetchone()["total_trains"]
    cur.execute("SELECT COUNT(*) AS total_bookings FROM bookings")
    total_bookings = cur.fetchone()["total_bookings"]
    cur.execute("SELECT COUNT(*) AS total_cancelled FROM cancellations")
    total_cancelled = cur.fetchone()["total_cancelled"]
    conn.close()
    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_trains=total_trains,
        total_bookings=total_bookings,
        total_cancelled=total_cancelled,
    )


@admin_bp.route("/admin/trains", methods=["GET", "POST"])
def admin_trains():
    if request.method == "POST":
        train_number = (request.form.get("train_number") or "").strip()
        train_name = (request.form.get("train_name") or "").strip()
        source = (request.form.get("source") or "").strip()
        destination = (request.form.get("destination") or "").strip()
        departure_time = request.form.get("departure_time")
        arrival_time = request.form.get("arrival_time")
        duration = request.form.get("duration")
        fare = request.form.get("fare")
        total_seats = request.form.get("total_seats")
        if not all([train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats]):
            flash("All train fields are required.", "danger")
            return redirect(url_for("admin.dashboard"))
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO trains (train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats, available_seats, class_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'General')",
            (train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats, total_seats),
        )
        conn.commit()
        conn.close()
        flash("Train added successfully.", "success")
        return redirect(url_for("admin.dashboard"))
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM trains ORDER BY departure_time")
    trains = cur.fetchall()
    conn.close()
    return render_template("admin/trains.html", trains=[dict(r) for r in trains])


@admin_bp.route("/api/admin/trains", methods=["POST"])
def api_add_train():
    payload = request.get_json(silent=True) or request.form
    if not session.get("user") or session["user"].get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized."}), 401
    required = ["train_number", "train_name", "source", "destination", "departure_time", "arrival_time", "duration", "fare", "total_seats"]
    if not all(payload.get(field) for field in required):
        return jsonify({"success": False, "message": "Missing required train details."}), 400
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO trains (train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats, available_seats, class_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'General')",
        (payload["train_number"], payload["train_name"], payload["source"], payload["destination"], payload["departure_time"], payload["arrival_time"], payload["duration"], payload["fare"], payload["total_seats"], payload["total_seats"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Train added."})


@admin_bp.route("/api/admin/trains/<int:train_id>", methods=["PUT", "DELETE"])
def api_update_delete_train(train_id):
    if not session.get("user") or session["user"].get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized."}), 401
    conn = db_connection()
    cur = conn.cursor()
    if request.method == "DELETE":
        cur.execute("DELETE FROM trains WHERE id = ?", (train_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Train deleted."})
    payload = request.get_json(silent=True) or request.form
    cur.execute(
        "UPDATE trains SET train_number = ?, train_name = ?, source = ?, destination = ?, departure_time = ?, arrival_time = ?, duration = ?, fare = ?, total_seats = ?, available_seats = ? WHERE id = ?",
        (payload.get("train_number"), payload.get("train_name"), payload.get("source"), payload.get("destination"), payload.get("departure_time"), payload.get("arrival_time"), payload.get("duration"), payload.get("fare"), payload.get("total_seats"), payload.get("total_seats"), train_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Train updated."})
