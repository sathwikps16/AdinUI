from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from flask_cors import CORS
from requests.auth import HTTPBasicAuth
from EnDe import PasswordEncrypter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# MongoDB connection
client = MongoClient("mongodb+srv://net-bot:test123@cluster0.uuwhk.mongodb.net/")  
db = client['TicketingSystemDB']  
collection = db['TicketingSystem']  

def verify_jira_credentials(JIRA_URL, JIRA_USER, JIRA_API_TOKEN):
    """
    Verify Jira credentials using the 'myself' endpoint.

    Args:
        JIRA_URL (str): The Jira instance URL.
        JIRA_USER (str): The Jira user's email or username.
        JIRA_API_TOKEN (str): The Jira API token.

    Returns:
        bool: True if credentials are valid, False otherwise.
        dict: User data if valid, error message if invalid.
    """
    url = f"{JIRA_URL}/rest/api/2/myself"
    
    try:
        response = requests.get(url, auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN))
        if response.status_code == 200:
            # Valid credentials
            return True, response.json()
        else:
            # Invalid credentials
            return False, f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Exception occurred: {e}"

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """
    Authenticate Jira credentials sent from frontend.

    Returns:
        JSON response: Success or failure message with relevant data.
    """
    data = request.get_json()
    JIRA_URL = data.get('instanceUrl')
    JIRA_USER = data.get('username')
    JIRA_API_TOKEN = data.get('password')  # API token sent as password

    if not JIRA_URL or not JIRA_USER or not JIRA_API_TOKEN:
        return jsonify({"success": False, "message": "Please provide all required fields."})

    # Verify credentials
    is_valid, result = verify_jira_credentials(JIRA_URL, JIRA_USER, JIRA_API_TOKEN)
    if is_valid:
        # Send success response with token (or any other info if needed)
        return jsonify({"success": True, "message": "Authentication successful!", "token": "example-token"})
    else:
        return jsonify({"success": False, "message": result})

@app.route('/save', methods=['POST'])
def save_credentials():
    """
    Save valid Jira credentials into MongoDB.

    Returns:
        JSON response: Success or failure message.
    """
    data = request.get_json()
    token = request.headers.get('Authorization')
    
    if not token or token != "Bearer example-token":  # Check if token matches (in reality, validate token properly)
        return jsonify({"success": False, "message": "Unauthorized access. Please authenticate first."})
    
    JIRA_URL = data.get('instance_url')
    JIRA_USER = data.get('username')
    JIRA_API_TOKEN = data.get('password')
    ENCRYPTED_TOKEN = PasswordEncrypter.encrypt_password(JIRA_API_TOKEN)

    # Save to MongoDB
    credentials = {
        "system": "Jira",
        "instance_url": JIRA_URL,
        "username": JIRA_USER,
        "password": ENCRYPTED_TOKEN,
    }

    try:
        collection.insert_one(credentials)
        return jsonify({"success": True, "message": "Data saved successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error saving data: {e}"})


if __name__ == "__main__":
    app.run(debug=True, port=5102)
