import re


# Clean text for better embeddings
def clean_text(text):

    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Extract keywords (basic NLP)
def extract_keywords(text):

    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return list(set(words[:15]))


# Safe filename handling
def sanitize_filename(filename):

    return filename.replace(" ", "_").lower()