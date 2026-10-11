from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if not name or not email or not password:
            flash("Please fill all required fields.", "danger")
            return render_template("register.html")
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            conn.close()
            flash("This email is already registered.", "danger")
            return render_template("register.html")
        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'user')", (name, email, hashed))
        conn.commit()
        conn.close()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        if not user or not check_password_hash(user["password"], password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")
        session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}
        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("trains.search"))
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND role = 'admin'", (email,))
        admin = cur.fetchone()
        conn.close()
        if admin and check_password_hash(admin["password"], password):
            session["user"] = {"id": admin["id"], "name": admin["name"], "email": admin["email"], "role": admin["role"]}
            return redirect(url_for("admin.dashboard"))
        flash("Invalid admin credentials.", "danger")
    return render_template("admin/login.html")
