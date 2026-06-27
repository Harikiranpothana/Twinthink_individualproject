from flask import Blueprint, request, jsonify

from services.rag_service import retrieve_context

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/ask", methods=["POST"])
def ask_question():

    data = request.get_json()

    question = data.get("question")

    if not question:
        return jsonify({
            "status": "error",
            "message": "Question is required"
        }), 400

    context = retrieve_context(question)

    return jsonify({
        "status": "success",
        "question": question,
        "retrieved_context": context
    })