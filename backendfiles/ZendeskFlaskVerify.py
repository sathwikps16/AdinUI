from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient
from EnDe import PasswordEncrypter

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
client = MongoClient("mongodb+srv://net-bot:test123@cluster0.uuwhk.mongodb.net/")
db = client['TicketingSystemDB']  
collection = db['TicketingSystem'] 

# Helper function to verify Zendesk credentials
def verify_zendesk_credentials(instance_url, admin_email, api_token):
    url = f"{instance_url}/api/v2/users/me.json"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, auth=HTTPBasicAuth(f"{admin_email}/token", api_token), headers=headers)
        if response.status_code == 200:
            user_data = response.json().get('user', {})
            role = user_data.get('role', 'unknown')
            print(role)
            if role == 'admin':
                return True, "Admin credentials verified successfully."
            else:
                return False, f"Your role is '{role}', but admin privileges are required."
        elif response.status_code == 401:
            return False, "Invalid credentials: Unauthorized access."
        else:
            return False, f"Unexpected error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Error during API call: {str(e)}"

# Endpoint to authenticate Zendesk credentials
@app.route('/zendesk/authenticate', methods=['POST'])
def zendesk_authenticate():
    data = request.json
    instance_url = data.get('instance_url')
    admin_id = data.get('admin_id')
    api_token = data.get('api_token')

    # Basic validation
    if not instance_url or not admin_id or not api_token:
        return jsonify({"success": False, "message": "Please provide all required fields."}), 400

    is_valid, message = verify_zendesk_credentials(instance_url, admin_id, api_token)
    if is_valid:
        return jsonify({"success": True, "message": message, "token": "zendesk-example-token"})
    else:
        return jsonify({"success": False, "message": message})

# Endpoint to save data in MongoDB
@app.route('/zendesk/save', methods=['POST'])
def save_data():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header.split()[1] != "zendesk-example-token":
        return jsonify({"success": False, "message": "Unauthorized access."}), 401

    data = request.get_json()
    instance_url = data.get("instance_url")
    email = data.get("admin_id")
    api_token = data.get("api_token")
    encrypt_token = PasswordEncrypter.encrypt_password(api_token)

    if not instance_url or not email or not api_token:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        # Save the data to MongoDB
        document = {
            "System": "Zendesk",
            "instance_url": instance_url,
            "email": email,
            "api_token": encrypt_token
        }
        collection.insert_one(document)
        return jsonify({"success": True, "message": "Data saved successfully!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5104)
