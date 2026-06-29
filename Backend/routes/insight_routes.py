from flask import Blueprint, request, jsonify
import sqlite3
from collections import Counter

from models.database import DB_PATH
from services.vector_service import search_similar_chunks
from services.insight_service import generate_insights

insight_bp = Blueprint("insight", __name__)


# =========================
# DB HELPER
# =========================
def fetch_all(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


# =====================================================
# 1. QUESTION-BASED INSIGHTS (YOUR EXISTING FEATURE)
# =====================================================
@insight_bp.route("/insights", methods=["POST"])
def insights():

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "question required"}), 400

    # FAISS / VECTOR SEARCH
    chunks = search_similar_chunks(question)

    # AI INSIGHT GENERATION
    insights = generate_insights(chunks)

    return jsonify({
        "status": "success",
        "insights": insights,
        "context": chunks
    })


# =====================================================
# 2. SYSTEM-WIDE INSIGHTS DASHBOARD (NEW UPGRADE)
# =====================================================
@insight_bp.route("/api/insights/dashboard", methods=["GET"])
def dashboard_insights():

    # =========================
    # CHAT ANALYSIS
    # =========================
    chats = fetch_all("SELECT user_question, timestamp FROM chat_history")

    questions = [c[0] for c in chats]
    timestamps = [c[1] for c in chats]

    top_questions = Counter(questions).most_common(5)

    # Activity per day
    activity_map = {}
    for t in timestamps:
        day = t.split("T")[0] if "T" in t else t.split(" ")[0]
        activity_map[day] = activity_map.get(day, 0) + 1

    activity_graph = [
        {"date": k, "count": v} for k, v in activity_map.items()
    ]

    # =========================
    # DOCUMENT ANALYSIS
    # =========================
    docs = fetch_all("SELECT filename FROM documents")

    doc_types = Counter([
        d[0].split(".")[-1] for d in docs if d[0]
    ])

    document_stats = dict(doc_types)

    # =========================
    # MEMORY ANALYSIS
    # =========================
    memory = fetch_all("SELECT event_text FROM memory_timeline")

    memory_insights = [
        m[0] for m in memory if m[0]
    ][-5:]  # last 5 events

    # =========================
    # FINAL RESPONSE
    # =========================
    return jsonify({
        "status": "success",
        "top_questions": [
            {"text": q, "count": c} for q, c in top_questions
        ],
        "activity_graph": activity_graph,
        "document_stats": document_stats,
        "memory_insights": memory_insights
    })