from flask import Blueprint, request, jsonify
from services.vector_service import search_similar_chunks
from services.insight_service import generate_insights

insight_bp = Blueprint("insight", __name__)


@insight_bp.route("/insights", methods=["POST"])
def insights():

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "question required"}), 400

    chunks = search_similar_chunks(question)

    insights = generate_insights(chunks)

    return jsonify({
        "status": "success",
        "insights": insights,
        "context": chunks
    })