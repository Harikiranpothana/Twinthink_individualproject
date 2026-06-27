import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_answer(question, context_chunks):

    try:

        if not context_chunks:
            return "I don't know based on provided data."

        context_text = "\n\n".join(context_chunks)

        prompt = f"""
You are TwinThink AI, an intelligent assistant.

Use ONLY the context below to answer the question.
If answer is not found, say: "I don't know based on provided data."

-----------------------
CONTEXT:
{context_text}
-----------------------

QUESTION:
{question}

Give a clear, structured, human-like answer.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error generating response: {str(e)}"