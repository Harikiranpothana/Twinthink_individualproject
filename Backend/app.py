from flask import Flask
from flask_cors import CORS
import os

app.register_blueprint(chat_bp)
from routes.upload_routes import upload_bp

app = Flask(__name__)
CORS(app)

# Create uploads folder automatically
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Register routes
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)
# Home Route
@app.route('/')
def home():
    return {
        "status": "success",
        "message": "TwinThink Backend Running Successfully"
    }

# Health Check Route
@app.route('/health')
def health():
    return {
        "server": "running",
        "backend": "TwinThink API Server"
    }

if __name__ == '__main__':
    app.run(debug=True)