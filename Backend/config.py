import os

# -------------------------
# Folder where uploaded files will be stored
# -------------------------
UPLOAD_FOLDER = "uploads"

# -------------------------
# Allowed file types
# -------------------------
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# -------------------------
# SQLite database path
# -------------------------
DATABASE_PATH = "database/metadata.db"

# -------------------------
# FAISS index folder
# -------------------------
FAISS_FOLDER = "database/faiss_index"

# -------------------------
# Gemini API Key (from .env)
# -------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")