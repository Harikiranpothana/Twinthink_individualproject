from services.vector_service import search_similar_chunks
from services.gemini_service import generate_answer
from models.database import save_query


def get_rag_response(question):

    # 1. Retrieve context
    context_chunks = search_similar_chunks(question)

    if not context_chunks:
        return {
            "answer": "I don't know based on provided data.",
            "context": []
        }

    # 2. Generate AI answer (Gemini)
    answer = generate_answer(question, context_chunks)

    # 3. Save query to database (memory layer)
    save_query(question, context_chunks)

    return {
        "answer": answer,
        "context": context_chunks
    }