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

# =========================
# CORS CONFIG (SAFE FOR FRONTEND)
# =========================
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

# =========================
# Create Required Folders
# =========================
UPLOAD_FOLDER = "uploads"
DATABASE_FOLDER = "database"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# =========================
# INIT DATABASE (IMPORTANT FIX)
# =========================
# ⚠️ CHANGE THIS IF YOUR FILE IS DIFFERENT
try:
    from models.database import init_db   # <-- FIXED (most common structure)
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print("❌ Database init failed:", e)

# =========================
# IMPORT BLUEPRINTS
# =========================
from routes.upload_routes import upload_bp
from routes.chat_routes import chat_bp
from routes.insight_routes import insight_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp

# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(insight_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

# =========================
# HOME ROUTE
# =========================
@app.route("/")
def home():
    return {
        "status": "success",
        "message": "TwinThink Backend Running Successfully 🚀"
    }

# =========================
# HEALTH CHECK ROUTE
# =========================
@app.route("/health")
def health():
    return {
        "status": "success",
        "server": "running",
        "backend": "TwinThink API Server"
    }

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )