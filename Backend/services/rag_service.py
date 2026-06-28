from services.vector_service import search_similar_chunks
from models.database import save_query


def generate_answer(question, context_chunks):

    if not context_chunks:
        return "I don't know based on provided data."

    context_text = "\n\n".join(context_chunks)

    answer = f"""
Based on your uploaded documents:

{context_text}

---

Question: {question}

Answer: The relevant information above is extracted from your knowledge base.
"""

    return answer


def get_rag_response(question):

    # 1. Retrieve context
    context_chunks = search_similar_chunks(question)

    # 2. Handle empty context
    if not context_chunks:
        return {
            "answer": "I don't know based on provided data.",
            "context": []
        }

    # 3. Generate answer (offline mode)
    answer = generate_answer(question, context_chunks)

    # 4. Save query (memory layer)
    save_query(question, context_chunks)

    return {
        "answer": answer,
        "context": context_chunks
    }