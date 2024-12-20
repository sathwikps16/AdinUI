# from flask import Flask, redirect, url_for, session, jsonify, send_file, request
# from flask_cors import CORS
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from google.auth.transport.requests import Request
# import os
# import io

# app = Flask(__name__)
# # Configure CORS to allow credentials
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# # Use a proper secret key
# app.secret_key = os.urandom(24)  

# # Ensure the downloads directory exists
# os.makedirs("downloads", exist_ok=True)

# # OAuth configuration
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# CLIENT_SECRETS_FILE = "client_secrets.json"
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# REDIRECT_URI = "http://localhost:5000/callback"
# FRONTEND_URL = "http://localhost:3000"

# @app.route("/")
# def home():
#     return "Google Drive File Listing Service"

# @app.route("/authorize")
# def authorize():
#     flow = Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE,
#         scopes=SCOPES,
#         redirect_uri=REDIRECT_URI
#     )
#     # Tell the user to select an account and grant permissions
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true'
#     )
    
#     # Store the state so the callback can verify the auth server response.
#     session['state'] = state
    
#     return redirect(authorization_url)

# @app.route("/callback")
# def callback():
#     # Specify the state when creating the flow in the callback so that it can
#     # verify the authorization server response.
#     state = session['state']
    
#     flow = Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE, 
#         scopes=SCOPES, 
#         state=state,
#         redirect_uri=REDIRECT_URI
#     )

#     # Use the authorization server's response to fetch the OAuth 2.0 tokens.
#     flow.fetch_token(authorization_response=request.url)

#     # Store credentials in the session
#     credentials = flow.credentials
#     session['credentials'] = {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }

#     # Redirect to frontend
#     return redirect(f"http://localhost:3000/google-drive")

# @app.route("/logout")
# def logout():
#     # Clear the session
#     session.clear()
    
#     # Redirect to frontend login page or home
#     return jsonify({"status": "logged_out", "redirect": FRONTEND_URL})

# @app.route("/list-files")
# def list_files():
#     # Check if credentials exist in session
#     if 'credentials' not in session:
#         return jsonify({"error": "Not authorized"}), 401
    
#     try:
#         # Reconstruct credentials from session
#         creds = Credentials(
#             token=session['credentials']['token'],
#             refresh_token=session['credentials']['refresh_token'],
#             token_uri=session['credentials']['token_uri'],
#             client_id=session['credentials']['client_id'],
#             client_secret=session['credentials']['client_secret'],
#             scopes=session['credentials']['scopes']
#         )

#         # Refresh the token if it's expired
#         if creds.expired and creds.refresh_token:
#             creds.refresh(Request())
            
#             # Update session with new credentials
#             session['credentials'].update({
#                 'token': creds.token,
#                 'refresh_token': creds.refresh_token
#             })

#         # Build Drive service
#         drive_service = build('drive', 'v3', credentials=creds)
        
#         # List files
#         results = drive_service.files().list(
#             pageSize=50, 
#             fields="files(id, name, mimeType, size)"
#         ).execute()
        
#         items = results.get('files', [])
#         return jsonify(items)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/download/<file_id>")
# def download_file(file_id):
#     # Check if credentials exist in session
#     if 'credentials' not in session:
#         return jsonify({"error": "Not authorized"}), 401
    
#     try:
#         # Reconstruct credentials
#         creds = Credentials(
#             token=session['credentials']['token'],
#             refresh_token=session['credentials']['refresh_token'],
#             token_uri=session['credentials']['token_uri'],
#             client_id=session['credentials']['client_id'],
#             client_secret=session['credentials']['client_secret'],
#             scopes=session['credentials']['scopes']
#         )

#         # Refresh token if expired
#         if creds.expired and creds.refresh_token:
#             creds.refresh(Request())
            
#             # Update session with new credentials
#             session['credentials'].update({
#                 'token': creds.token,
#                 'refresh_token': creds.refresh_token
#             })

#         # Build Drive service
#         drive_service = build('drive', 'v3', credentials=creds)
        
#         # Get file metadata
#         file_metadata = drive_service.files().get(fileId=file_id).execute()
        
#         # Check if file can be downloaded
#         if file_metadata.get('mimeType') == 'application/vnd.google-apps.folder':
#             return jsonify({"error": "Cannot download a folder"}), 400
        
#         # Prepare download
#         request = drive_service.files().get_media(fileId=file_id)
#         file_name = file_metadata.get('name', f'{file_id}.bin')
        
#         # Download file
#         file_path = os.path.join("downloads", file_name)
#         with open(file_path, "wb") as file:
#             downloader = MediaIoBaseDownload(file, request)
#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()
        
#         return send_file(file_path, as_attachment=True, download_name=file_name)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, redirect, url_for, session, jsonify, send_file, request
from flask_cors import CORS
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from pymilvus import connections, Collection, utility
import os
import io
import fitz  # PyMuPDF for PDF processing
import pytesseract  # For image OCR
from PIL import Image
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# Rest of your imports and configurations remain the same...

@app.route("/upload-to-milvus/<file_id>", methods=['POST'])
def upload_to_milvus(file_id):
    try:
        # Check authorization
        if 'credentials' not in session:
            return jsonify({"error": "Not authorized"}), 401
        
        # Get collection name from form data
        collection_name = request.form.get('collection')
        if not collection_name:
            return jsonify({"error": "Collection name is required"}), 400
            
        if collection_name not in ['hr_collection', 'finance_collection', 'it_collection', 'other_collection']:
            return jsonify({"error": "Invalid collection name"}), 400

        # Reconstruct credentials
        creds = Credentials(
            token=session['credentials']['token'],
            refresh_token=session['credentials']['refresh_token'],
            token_uri=session['credentials']['token_uri'],
            client_id=session['credentials']['client_id'],
            client_secret=session['credentials']['client_secret'],
            scopes=session['credentials']['scopes']
        )

        # Refresh token if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            session['credentials'].update({
                'token': creds.token,
                'refresh_token': creds.refresh_token
            })

        # Build Drive service
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Get file metadata
        file_metadata = drive_service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name')
        mime_type = file_metadata.get('mimeType')
        
        # Create downloads directory if it doesn't exist
        os.makedirs("downloads", exist_ok=True)
        
        # Download file
        request = drive_service.files().get_media(fileId=file_id)
        file_path = os.path.join("downloads", file_name)
        
        with open(file_path, "wb") as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        
        # Extract text based on file type
        text = ""
        try:
            if mime_type == 'application/pdf':
                text = extract_text_from_pdf(file_path)
            elif mime_type.startswith('image/'):
                text = extract_text_from_image(file_path)
            elif mime_type == 'text/plain':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            else:
                # Clean up downloaded file
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({"error": f"Unsupported file type: {mime_type}"}), 400
                
            # Generate embedding
            embedding = get_embedding(text)
            
            # Insert into Milvus
            collection = Collection(collection_name)
            collection.insert([
                [file_name],  # filename
                [text],       # content
                [embedding.tolist()]  # embedding
            ])
            
            # Clean up downloaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return jsonify({
                "status": "success", 
                "message": f"File {file_name} uploaded to {collection_name}"
            })
            
        except Exception as e:
            # Clean up downloaded file in case of error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e
            
    except Exception as e:
        print(f"Error in upload_to_milvus: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Rest of your endpoints remain the same...

if __name__ == "__main__":
    app.run(debug=True)