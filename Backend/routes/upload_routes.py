from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Check file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
def upload_file():

    # Check if file exists in request
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file part in request"
        }), 400

    file = request.files['file']

    # Check if user selected file
    if file.filename == '':
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400

    # Validate and save file
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(file_path)

        return jsonify({
            "status": "success",
            "message": "File uploaded successfully",
            "filename": filename
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid file type"
    }), 400