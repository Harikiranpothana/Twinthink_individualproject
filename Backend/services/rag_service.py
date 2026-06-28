from services.vector_service import search_similar_chunks
from models.database import save_query, save_chat


# ------------------------------------------------
# Generate Answer (Offline Mode)
# ------------------------------------------------
def generate_answer(question, context_chunks):

    if not context_chunks:
        return "I don't know based on the provided documents."

    context_text = "\n\n".join(context_chunks)

    answer = f"""
Based on your uploaded documents:

{context_text}

------------------------------------------------

Question:
{question}

Answer:
The above information was retrieved from your knowledge base.
"""

    return answer.strip()


# ------------------------------------------------
# Main RAG Pipeline
# ------------------------------------------------
def get_rag_response(question):

    # 1. Retrieve relevant chunks from FAISS
    context_chunks = search_similar_chunks(question)

    # 2. Handle no results
    if not context_chunks:

        answer = "I don't know based on the provided documents."

        # Save chat history
        save_chat(question, answer)

        return {
            "answer": answer,
            "context": []
        }

    # 3. Generate answer
    answer = generate_answer(question, context_chunks)

    # 4. Save query analytics
    save_query(question, context_chunks)

    # 5. Save complete chat history
    save_chat(question, answer)

    # 6. Return response
    return {
        "answer": answer,
        "context": context_chunks
    }