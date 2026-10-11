from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from database.db import db_connection
from dsa.hash_table import HashTable
from dsa.queue import RailwayQueue
from dsa.sorting import sort_trains

trains_bp = Blueprint("trains", __name__)


@trains_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        source = (request.form.get("source") or "").strip()
        destination = (request.form.get("destination") or "").strip()
        journey_date = request.form.get("journey_date") or ""
        travel_class = request.form.get("class_name") or ""
        sort_by = request.form.get("sort_by") or "departure_time"
        if not source or not destination or not journey_date:
            flash("Source, destination, and date are required.", "danger")
            return render_template("search.html")
        return redirect(
            url_for(
                "trains.results",
                source=source,
                destination=destination,
                journey_date=journey_date,
                class_name=travel_class,
                sort_by=sort_by,
            )
        )
    return render_template("search.html")


@trains_bp.route("/results")
def results():
    source = (request.args.get("source") or "").strip()
    destination = (request.args.get("destination") or "").strip()
    journey_date = request.args.get("journey_date") or ""
    travel_class = request.args.get("class_name") or "General"
    sort_by = request.args.get("sort_by") or "departure_time"
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM trains WHERE source LIKE ? AND destination LIKE ? ORDER BY departure_time",
        (f"%{source}%", f"%{destination}%"),
    )
    rows = cur.fetchall()
    conn.close()
    train_list = [dict(r) for r in rows]
    sorted_list = sort_trains(train_list, sort_by)
    return render_template("results.html", trains=sorted_list, journey_date=journey_date, travel_class=travel_class, source=source, destination=destination)


@trains_bp.route("/booking", methods=["GET", "POST"])
def booking():
    if not session.get("user"):
        flash("Please log in to make a booking.", "danger")
        return redirect(url_for("auth.login"))
    train_id = request.args.get("train_id") or request.form.get("train_id")
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM trains WHERE id = ?", (train_id,))
    train = cur.fetchone()
    conn.close()
    if not train:
        flash("Selected train not found.", "danger")
        return redirect(url_for("trains.search"))

    if request.method == "POST":
        passenger_name = (request.form.get("passenger_name") or "").strip()
        age = request.form.get("age") or ""
        gender = request.form.get("gender") or ""
        journey_date = request.form.get("journey_date") or ""
        class_name = request.form.get("class_name") or "General"
        if not all([passenger_name, age, gender, journey_date]):
            flash("All passenger details are required.", "danger")
            return render_template("booking.html", train=dict(train), journey_date=journey_date)
        if int(age) < 1 or int(age) > 120:
            flash("Age must be valid.", "danger")
            return render_template("booking.html", train=dict(train), journey_date=journey_date)
        if journey_date < datetime.utcnow().strftime("%Y-%m-%d"):
            flash("Past dates are not allowed for booking.", "danger")
            return render_template("booking.html", train=dict(train), journey_date=journey_date)

        pnr = str(__import__("random").randint(1000000000, 9999999999))
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT available_seats FROM trains WHERE id = ?", (train_id,))
        seat_row = cur.fetchone()
        if seat_row and seat_row["available_seats"] > 0:
            seat_number = f"{train['train_number']}-{__import__('random').randint(1, 100)}"
            cur.execute(
                "INSERT INTO bookings (pnr, user_id, train_id, passenger_name, age, gender, journey_date, class, seat_number, status, booking_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'CONFIRMED', datetime('now'))",
                (pnr, session["user"]["id"], train_id, passenger_name, int(age), gender, journey_date, class_name, seat_number),
            )
            cur.execute("UPDATE trains SET available_seats = available_seats - 1 WHERE id = ?", (train_id,))
            conn.commit()
            conn.close()
            flash("Booking successful!", "success")
            return redirect(url_for("trains.confirmation", pnr=pnr))
        conn.close()
        flash("No seats available. You have been added to the waiting list.", "warning")
        return redirect(url_for("trains.confirmation", pnr=pnr))

    return render_template("booking.html", train=dict(train))


@trains_bp.route("/confirmation/<pnr>")
def confirmation(pnr):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT b.*, t.train_number, t.train_name, t.source, t.destination, t.departure_time, t.arrival_time, t.fare FROM bookings b JOIN trains t ON t.id = b.train_id WHERE b.pnr = ?",
        (pnr,),
    )
    booking = cur.fetchone()
    conn.close()
    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("trains.search"))
    return render_template("confirmation.html", booking=dict(booking))


@trains_bp.route("/my-bookings")
def my_bookings():
    if not session.get("user"):
        flash("Please log in to view bookings.", "danger")
        return redirect(url_for("auth.login"))
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT b.*, t.train_number, t.train_name, t.source, t.destination FROM bookings b JOIN trains t ON t.id = b.train_id WHERE b.user_id = ? ORDER BY b.booking_time DESC",
        (session["user"]["id"],),
    )
    rows = cur.fetchall()
    conn.close()
    return render_template("bookings.html", bookings=[dict(r) for r in rows])


@trains_bp.route("/pnr", methods=["GET", "POST"])
def pnr_lookup():
    if request.method == "POST":
        pnr = (request.form.get("pnr") or "").strip()
        if not pnr:
            flash("Please enter a PNR number.", "danger")
            return render_template("pnr.html")
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT b.*, t.train_number, t.train_name, t.source, t.destination, t.departure_time, t.arrival_time FROM bookings b JOIN trains t ON t.id = b.train_id WHERE b.pnr = ?",
            (pnr,),
        )
        booking = cur.fetchone()
        conn.close()
        if not booking:
            flash("No booking found for the entered PNR.", "danger")
            return render_template("pnr.html")
        return render_template("pnr.html", booking=dict(booking))
    return render_template("pnr.html")


@trains_bp.route("/cancel", methods=["GET", "POST"]) 
def cancel_ticket():
    if request.method == "POST":
        pnr = (request.form.get("pnr") or "").strip()
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM bookings WHERE pnr = ?", (pnr,))
        booking = cur.fetchone()
        if not booking:
            conn.close()
            flash("Booking not found.", "danger")
            return render_template("cancel.html")
        cur.execute("UPDATE bookings SET status = 'CANCELLED' WHERE pnr = ?", (pnr,))
        cur.execute("UPDATE trains SET available_seats = available_seats + 1 WHERE id = ?", (booking["train_id"],))
        cur.execute("INSERT INTO cancellations (pnr, cancellation_time, refund_amount, status) VALUES (?, datetime('now'), 0, 'CANCELLED')", (pnr,))
        conn.commit()
        conn.close()
        flash(f"Ticket {pnr} cancelled successfully.", "success")
        return render_template("cancel.html", pnr=pnr)
    return render_template("cancel.html")
