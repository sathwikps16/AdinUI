from flask import Flask, request, jsonify
from onedrive import OneDriveHandler
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Allow CORS for communication with React frontend

logging.basicConfig(level=logging.INFO)
one_drive_handler = OneDriveHandler()

@app.route('/auth', methods=['GET'])
def authenticate():
    """Authenticate with OneDrive and get an access token."""
    try:
        if one_drive_handler.get_token():
            return jsonify({"message": "Authentication successful"}), 200
        return jsonify({"error": "Authentication failed"}), 401
    except Exception as e:
        logging.error(f"Authentication error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/list-files', methods=['GET'])
def list_files():
    """List files from OneDrive."""
    try:
        files = one_drive_handler.list_files()
        return jsonify(files), 200
    except Exception as e:
        logging.error(f"Error listing files: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/download-file', methods=['POST'])
def download_file():
    """Download a file by name and upload it to Milvus."""
    try:
        data = request.json
        if not data or not data.get("file_name") or not data.get("department"):
            return jsonify({"error": "File name and department are required"}), 400

        file_name = data["file_name"]
        department = data["department"]

        if one_drive_handler.download_file_by_name(file_name, department):
            return jsonify({"message": f"File '{file_name}' uploaded successfully"}), 200
        return jsonify({"error": f"File '{file_name}' not found"}), 404
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
