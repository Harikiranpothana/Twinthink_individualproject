from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# =========================
# Load Environment Variables
# =========================
load_dotenv()

# =========================
# Create Flask App
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# Create Required Folders
# =========================
UPLOAD_FOLDER = "uploads"
DATABASE_FOLDER = "database"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# =========================
# Initialize Database
# =========================
from models.database import init_db
init_db()

# =========================
# Import Blueprints
# =========================
from routes.upload_routes import upload_bp
from routes.chat_routes import chat_bp
from routes.insight_routes import insight_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp

# =========================
# Register Blueprints
# =========================
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(insight_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

# =========================
# Home Route
# =========================
@app.route("/")
def home():

    return {
        "status": "success",
        "message": "TwinThink Backend Running Successfully 🚀"
    }


# =========================
# Health Check Route
# =========================
@app.route("/health")
def health():

    return {
        "status": "success",
        "server": "running",
        "backend": "TwinThink API Server"
    }


# =========================
# Run Flask Server
# =========================
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )