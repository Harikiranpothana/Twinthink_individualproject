from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime

from services.file_processor import extract_text
from services.chunk_service import create_chunks
from services.embedding_service import generate_embeddings
from services.vector_service import save_to_faiss

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_PATH = "database/metadata.db"


# =========================
# FILE CHECK
# =========================
def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================
# SAVE TIMELINE EVENT
# =========================
def add_timeline_event(event_text, event_type="upload"):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memory_timeline
        (event_text, event_type, timestamp)
        VALUES (?, ?, ?)
    """, (
        event_text,
        event_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    print("✅ Timeline added:", event_text)


# =========================
# SAVE DOCUMENT INFO
# =========================
def save_document_info(filename, chunk_count):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents
        (filename, upload_time, chunk_count)
        VALUES (?, ?, ?)
    """, (
        filename,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        chunk_count
    ))

    conn.commit()
    conn.close()

    print(f"✅ Document saved: {filename}")


# =========================
# UPLOAD ROUTE
# =========================
@upload_bp.route('/upload', methods=['POST'])
def upload_file():

    try:

        files = request.files.getlist("files")

        if not files or files[0].filename == "":

            return jsonify({
                "success": False,
                "message": "No file uploaded"
            }), 400

        processed_files = []

        for file in files:

            if not allowed_file(file.filename):
                continue

            # -------------------------
            # SAVE FILE
            # -------------------------
            filename = secure_filename(file.filename)

            file_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            file.save(file_path)

            print(f"📄 Processing: {filename}")

            # -------------------------
            # EXTRACT TEXT
            # -------------------------
            extracted_text = extract_text(file_path)

            if not extracted_text:

                return jsonify({
                    "success": False,
                    "message":
                        f"Text extraction failed for {filename}"
                }), 500

            # -------------------------
            # CREATE CHUNKS
            # -------------------------
            chunks = create_chunks(extracted_text)

            if not chunks:

                return jsonify({
                    "success": False,
                    "message":
                        f"No chunks created for {filename}"
                }), 500

            # -------------------------
            # GENERATE EMBEDDINGS
            # -------------------------
            embeddings = generate_embeddings(chunks)

            if embeddings is None:

                return jsonify({
                    "success": False,
                    "message":
                        f"Embedding failed for {filename}"
                }), 500

            # -------------------------
            # SAVE TO FAISS
            # -------------------------
            save_to_faiss(chunks, embeddings)

            # -------------------------
            # SAVE TO DOCUMENTS TABLE
            # -------------------------
            save_document_info(
                filename,
                len(chunks)
            )

            # -------------------------
            # SAVE TO MEMORY TIMELINE
            # -------------------------
            add_timeline_event(
                f"📄 Uploaded document: {filename}",
                "upload"
            )

            # -------------------------
            # RESPONSE DATA
            # -------------------------
            processed_files.append({
                "filename": filename,
                "chunks": len(chunks)
            })

        return jsonify({
            "success": True,
            "message":
                "Documents processed successfully",
            "files": processed_files
        })

    except Exception as e:

        print("❌ UPLOAD ERROR:", str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500