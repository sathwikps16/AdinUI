from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from milvus_imple import MultiDepartmentVectorDB  # Assuming `upload.py` is in the same folder
from PIL import Image
import logging
 
app = Flask(__name__)
CORS(app)
 
# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
UPLOAD_FOLDER = './uploaded_files'  # Temporary folder for storing uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Initialize MultiDepartmentVectorDB instance
vector_db = MultiDepartmentVectorDB()
 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    department = request.form.get('department')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if department not in ['IT', 'FINANCE', 'HR', 'OTHERS']:
        return jsonify({"error": "Invalid department"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Check if the uploaded file is an image (by extension)
        is_image = filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))

        # Check if the uploaded file is a DOCX file
        is_docx = filename.lower().endswith(('doc'))

        try:
            # Upload file to Milvus (PDF, DOCX, or image)
            success = vector_db.upload_file_to_department(department, file_path, is_image or is_docx)
            if success:
                logger.info(f"Successfully uploaded {filename} to {department} collection")
                return jsonify({"message": f"Successfully uploaded {filename} to {department} collection"}), 200
            else:
                logger.error(f"File upload failed for {filename} in {department} collection")
                return jsonify({"error": "File upload failed"}), 500
        except Exception as e:
            logger.error(f"Error during file upload: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500


# Run the Flask app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)