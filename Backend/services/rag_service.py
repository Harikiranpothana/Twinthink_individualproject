from services.vector_service import search_similar_chunks
from models.database import save_query, save_chat


# =====================================================
# LOCAL ANSWER GENERATOR (NO API - CLEANED VERSION)
# =====================================================
def generate_answer(question, context_chunks):

    if not context_chunks:
        return "I don't know based on the provided documents."

    # =========================
    # CLEAN CONTEXT
    # =========================
    cleaned_chunks = []

    for c in context_chunks:
        c = c.replace("{", "").replace("}", "")
        c = c.replace("#", "")
        c = c.replace("printf", "")
        cleaned_chunks.append(c.strip())

    context_text = "\n".join(cleaned_chunks)

    # =========================
    # SIMPLE INTELLIGENT SUMMARY (NO API)
    # =========================
    answer = f"""
Based on your uploaded documents, the system found relevant information.

Key extracted content:
{context_text[:1200]}

------------------------------------------------

Question:
{question}

Summary:
The retrieved documents contain relevant technical information related to your query.
This is an offline RAG response (no AI model used yet).
"""

    return answer.strip()


# =====================================================
# MAIN RAG PIPELINE
# =====================================================
def get_rag_response(question):

    # 1. Retrieve relevant chunks
    context_chunks = search_similar_chunks(question)

    # 2. No results case
    if not context_chunks:

        answer = "I don't know based on the provided documents."

        save_chat(question, answer)

        return {
            "answer": answer,
            "context": []
        }

    # 3. Generate answer (cleaned version)
    answer = generate_answer(question, context_chunks)

    # 4. Save analytics (query tracking)
    save_query(question, context_chunks)

    # 5. Save chat history
    save_chat(question, answer)

    # 6. Return final response
    return {
        "answer": answer,
        "context": context_chunks
    }