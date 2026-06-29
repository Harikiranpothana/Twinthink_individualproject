# services/llm_service.py

import os


# =========================
# SWITCH CONTROL (IMPORTANT)
# =========================
USE_API = False  # 🔥 change to True later when Gemini is added


# =========================
# LOCAL FALLBACK GENERATOR (NO API)
# =========================
def local_generate_answer(question, context_chunks):

    if not context_chunks:
        return "I couldn't find relevant information in your documents."

    # simple clean join
    context_text = "\n".join(context_chunks)

    # extract lightweight "meaning"
    summary = f"""
Based on your documents, here is a simplified explanation:

{context_text[:1000]}

---

Question: {question}

This is a local fallback response (no AI API used yet).
It shows retrieved knowledge from your system.
"""

    return summary


# =========================
# API GENERATOR (FUTURE)
# =========================
def api_generate_answer(question, context_chunks):

    """
    This will be replaced later with Gemini / OpenAI
    """

    # placeholder for now
    return local_generate_answer(question, context_chunks)


# =========================
# MAIN FUNCTION (USE THIS EVERYWHERE)
# =========================
def generate_answer(question, context_chunks):

    if USE_API:
        return api_generate_answer(question, context_chunks)
    else:
        return local_generate_answer(question, context_chunks)