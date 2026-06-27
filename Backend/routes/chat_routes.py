from flask import Blueprint, request, jsonify
from services.rag_service import get_rag_response

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

    # 🔥 FULL RAG PIPELINE (FAISS + GEMINI + MEMORY)
    result = get_rag_response(question)

    return jsonify({
        "status": "success",
        "question": question,
        "answer": result["answer"],
        "retrieved_context": result["context"]
    })