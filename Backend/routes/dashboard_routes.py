from flask import Blueprint, jsonify
import sqlite3
import os

dashboard_bp = Blueprint("dashboard", __name__)

DB_PATH = "database/metadata.db"


def get_count(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    conn.close()
    return result


@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():

    total_docs = get_count("SELECT COUNT(*) FROM documents")
    total_queries = get_count("SELECT COUNT(*) FROM queries")

    return jsonify({
        "status": "success",
        "stats": {
            "total_documents": total_docs,
            "total_queries": total_queries
        },
        "system": "TwinThink AI Active"
    })