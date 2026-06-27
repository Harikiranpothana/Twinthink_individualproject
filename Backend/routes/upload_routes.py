from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from services.file_processor import extract_text

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

        # Extract text from uploaded document
        extracted_text = extract_text(file_path)

        return jsonify({
            "status": "success",
            "message": "File uploaded and processed successfully",
            "filename": filename,
            "text_length": len(extracted_text),
            "preview": extracted_text[:500]
        })

    return jsonify({
        "status": "error",
        "message": "Invalid file type"
    }), 400