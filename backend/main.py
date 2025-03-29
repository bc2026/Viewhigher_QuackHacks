from flask import Flask, request, jsonify, send_file, send_from_directory
import os

app = Flask(__name__, static_folder="static")

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "temp")

# Ensure temp folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    """Serve the index.html file from src/"""
    return send_file(os.path.join("../frontend/", "index.html"))

@app.route('/static/assets/<path:filename>')
def serve_static(filename):
    """Serve static files (images, CSS, etc.)"""
    return send_from_directory(os.path.join("../frontend/", "assets/"), filename)

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file uploads"""
    print("🔹 Received a request to upload a resume.")

    if 'resume' not in request.files:
        print("❌ Error: No file uploaded.")
        return jsonify({"error": "No file uploaded"}), 400

    resume = request.files['resume']
    print(f"📂 Received file: {resume.filename}")

    if resume.filename == '':
        print("❌ Error: No selected file.")
        return jsonify({"error": "No selected file"}), 400

    # Save the resume inside src/temp/
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    
    try:
        resume.save(file_path)
        print(f"✅ Resume saved to {file_path}")
        return jsonify({
            "message": "Resume uploaded successfully!",
            "resumeFile": resume.filename,
            "filePath": file_path
        })
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("✅ Flask server running on http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)
