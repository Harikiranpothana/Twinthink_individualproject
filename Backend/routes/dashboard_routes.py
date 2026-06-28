from flask import Blueprint, jsonify
import sqlite3

dashboard_bp = Blueprint("dashboard", __name__)

DB_PATH = "database/metadata.db"


# =========================
# Helper
# =========================
def get_count(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    conn.close()
    return result


# =========================
# Dashboard Stats
# =========================
@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({
        "status": "success",
        "stats": {
            "total_documents": get_count("SELECT COUNT(*) FROM documents"),
            "total_queries": get_count("SELECT COUNT(*) FROM queries"),
            "total_chats": get_count("SELECT COUNT(*) FROM chat_history"),
            "total_users": get_count("SELECT COUNT(*) FROM users")
        }
    })


# =========================
# FIXED MEMORY TIMELINE API
# (UNIFIED + FRONTEND COMPATIBLE)
# =========================
@dashboard_bp.route("/memory-timeline", methods=["GET"])
def memory_timeline():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timeline = []

    # -------------------------
    # Documents
    # -------------------------
    cursor.execute("SELECT filename, upload_time FROM documents")
    for filename, time in cursor.fetchall():
        timeline.append({
            "event_text": f"📄 Uploaded document: {filename}",
            "event_type": "upload",
            "timestamp": time
        })

    # -------------------------
    # Queries
    # -------------------------
    cursor.execute("SELECT question, timestamp FROM queries")
    for q, time in cursor.fetchall():
        timeline.append({
            "event_text": f"❓ Asked: {q}",
            "event_type": "query",
            "timestamp": time
        })

    # -------------------------
    # Chats
    # -------------------------
    cursor.execute("SELECT user_question, timestamp FROM chat_history")
    for q, time in cursor.fetchall():
        timeline.append({
            "event_text": f"💬 Chat: {q}",
            "event_type": "chat",
            "timestamp": time
        })

    conn.close()

    # sort newest first
    timeline.sort(key=lambda x: x["timestamp"], reverse=True)

    return jsonify({
        "status": "success",
        "timeline": timeline
    })