from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "database/metadata.db"


# =========================
# MEMORY TIMELINE API
# =========================
@app.route("/memory-timeline", methods=["GET"])
def get_memory_timeline():

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT event_text, event_type, timestamp
            FROM memory_timeline
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        timeline = [
            {
                "event_text": r[0],
                "event_type": r[1],
                "timestamp": r[2]
            }
            for r in rows
        ]

        return jsonify({
            "timeline": timeline
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500