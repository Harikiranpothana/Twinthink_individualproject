from pypdf import PdfReader
from docx import Document
import os


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    elif extension == ".txt":
        return extract_txt(file_path)

    else:
        raise ValueError("Unsupported file type")


# --------------------------
# PDF Extraction
# --------------------------
def extract_pdf(file_path):

    text = ""
    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return clean_text(text)


# --------------------------
# DOCX Extraction
# --------------------------
def extract_docx(file_path):

    text = ""
    document = Document(file_path)

    for para in document.paragraphs:
        text += para.text + "\n"

    return clean_text(text)


# --------------------------
# TXT Extraction
# --------------------------
def extract_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return clean_text(file.read())


# --------------------------
# TEXT CLEANING (IMPORTANT FIX)
# --------------------------
def clean_text(text):

    if not text:
        return ""

    # Normalize whitespace
    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    text = " ".join(text.split())

    return text.strip()