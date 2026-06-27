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


def extract_pdf(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx(file_path):

    text = ""

    document = Document(file_path)

    for para in document.paragraphs:
        text += para.text + "\n"

    return text


def extract_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()