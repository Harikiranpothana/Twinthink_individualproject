from flask import Flask
from flask_cors import CORS
import os

from dotenv import load_dotenv

# -------------------------
# Load environment variables FIRST
# -------------------------
load_dotenv()

# -------------------------
# Import Blueprints
# -------------------------
from routes.upload_routes import upload_bp
from routes.chat_routes import chat_bp

# -------------------------
# Flask App Init
# -------------------------
app = Flask(__name__)
CORS(app)

# -------------------------
# Auto-create uploads folder
# -------------------------
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------
# Register Blueprints
# -------------------------
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)

# -------------------------
# Home Route
# -------------------------
@app.route('/')
def home():
    return {
        "status": "success",
        "message": "TwinThink Backend Running Successfully 🚀"
    }

# -------------------------
# Health Check Route
# -------------------------
@app.route('/health')
def health():
    return {
        "server": "running",
        "backend": "TwinThink API Server"
    }

# -------------------------
# Run Server
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)