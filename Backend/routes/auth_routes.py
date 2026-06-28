from flask import Blueprint, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

DB_PATH = "database/metadata.db"


# -------------------------
# SIGNUP
# -------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, hashed_password))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()

        return jsonify({
            "status": "error",
            "message": "Email already exists"
        }), 400

    conn.close()

    return jsonify({
        "status": "success",
        "message": "Account created successfully"
    })


# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user[0],
                "username": user[1],
                "email": email
            }
        })

    return jsonify({
        "status": "error",
        "message": "Invalid email or password"
    }), 401