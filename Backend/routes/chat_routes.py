from flask import Blueprint, request, jsonify
from services.rag_service import get_rag_response
from models.database import get_chat_history, save_chat

chat_bp = Blueprint("chat", __name__)


# ==========================================
# ASK QUESTION ROUTE
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

    # =========================
    # GET RAG RESPONSE
    # =========================
    result = get_rag_response(question)

    answer = result.get("answer", "")
    context = result.get("context", [])

    # =========================
    # SAVE CHAT (IMPORTANT FOR INSIGHTS)
    # =========================
    save_chat(question, answer)

    return jsonify({
        "status": "success",
        "question": question,
        "answer": answer,
        "retrieved_context": context
    })


# ==========================================
# CHAT HISTORY ROUTE
# ==========================================
@chat_bp.route("/chat-history", methods=["GET"])
def chat_history():

    chats = get_chat_history()

    history = [
        {
            "question": q,
            "answer": a
        }
        for q, a in chats
    ]

    return jsonify({
        "status": "success",
        "history": history
    })