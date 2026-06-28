from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# -------------------------
# Load environment variables FIRST
# -------------------------
load_dotenv()

# -------------------------
# Flask App Init
# -------------------------
app = Flask(__name__)
CORS(app)

# -------------------------
# Config
# -------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

# -------------------------
# Initialize SQLite Database
# -------------------------
from models.database import init_db
init_db()

# -------------------------
# Import Blueprints
# -------------------------
from routes.upload_routes import upload_bp
from routes.chat_routes import chat_bp
from routes.insight_routes import insight_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp

# -------------------------
# Register Blueprints
# -------------------------
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(insight_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

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