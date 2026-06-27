from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from services.file_processor import extract_text
from services.chunk_service import create_chunks
from services.embedding_service import generate_embeddings
from services.vector_service import save_to_faiss

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file part in request"
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(file_path)

        extracted_text = extract_text(file_path)

        chunks = create_chunks(extracted_text)

        embeddings = generate_embeddings(chunks)

        save_to_faiss(chunks, embeddings)

        return jsonify({
            "status": "success",
            "message": "Document indexed successfully",
            "filename": filename,
            "total_chunks": len(chunks),
            "embedding_dimension": embeddings.shape[1]
        })

    return jsonify({
        "status": "error",
        "message": "Invalid file type"
    }), 400