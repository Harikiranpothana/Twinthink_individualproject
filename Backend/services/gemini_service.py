def generate_answer(question, context_chunks):

    context_text = "\n\n".join(context_chunks)

    if not context_text.strip():
        return "I don't know based on provided data."

    # 🧠 Simple extractive answer (NO API)
    answer = f"""
Based on your documents:

{context_text}

---

Question: {question}

Answer: The above information contains relevant details from your uploaded data.
"""

    return answer