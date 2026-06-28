from flask import Blueprint, request, jsonify
from services.rag_service import get_rag_response
from models.database import get_chat_history

chat_bp = Blueprint("chat", __name__)


# ==========================================
# Ask Question Route
# ==========================================
@chat_bp.route("/ask", methods=["POST"])
def ask_question():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    question = data.get("question")

    if not question:
        return jsonify({
            "status": "error",
            "message": "Question is required"
        }), 400

    # Get RAG response
    result = get_rag_response(question)

    return jsonify({
        "status": "success",
        "question": question,
        "answer": result["answer"],
        "retrieved_context": result["context"]
    })


# ==========================================
# Chat History Route
# ==========================================
@chat_bp.route("/chat-history", methods=["GET"])
def chat_history():

    chats = get_chat_history()

    history = []

    for question, answer in chats:
        history.append({
            "question": question,
            "answer": answer
        })

    return jsonify({
        "status": "success",
        "history": history
    })