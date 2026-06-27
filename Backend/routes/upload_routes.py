from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
def upload_file():

    print("Request Files:", request.files)

    if 'file' not in request.files:
        print("No file key found")

        return jsonify({
            "status": "error",
            "message": "No file part in request"
        }), 400

    file = request.files['file']

    print("Received filename:", file.filename)

    if file.filename == '':
        print("Filename is empty")

        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file_path = os.path.join(UPLOAD_FOLDER, filename)

        print("Saving file to:", file_path)

        file.save(file_path)

        return jsonify({
            "status": "success",
            "message": "File uploaded successfully",
            "filename": filename
        }), 200

    print("Invalid file type")

    return jsonify({
        "status": "error",
        "message": "Invalid file type"
    }), 400