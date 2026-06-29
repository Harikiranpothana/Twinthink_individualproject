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

    return answerimport re


def clean_text(text):
    """
    Removes noisy code-like content
    """

    # remove symbols that usually appear in code
    text = re.sub(r"[{}#<>;]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def generate_answer(question, context_chunks):

    if not context_chunks:
        return "I couldn't find relevant information in your documents."

    # =========================
    # CLEAN CHUNKS
    # =========================
    cleaned_chunks = [clean_text(c) for c in context_chunks]

    # filter useless chunks
    useful_chunks = [
        c for c in cleaned_chunks
        if len(c) > 30 and "printf" not in c
    ]

    if not useful_chunks:
        return "The documents contain technical programming content, but no clear explanation was found."

    # =========================
    # BUILD SIMPLE SUMMARY
    # =========================
    summary = "Based on your uploaded documents, the content includes:\n\n"

    # extract meaningful words
    keywords = set()

    for text in useful_chunks:
        words = text.split()
        for w in words:
            if w.isalpha() and len(w) > 5:
                keywords.add(w.lower())

    top_keywords = list(keywords)[:10]

    if top_keywords:
        summary += "- Topics like: " + ", ".join(top_keywords) + "\n\n"

    summary += f"Answer: The documents are related to the question '{question}', "
    summary += "but detailed explanation requires higher-level summarization (AI layer)."

    return summary