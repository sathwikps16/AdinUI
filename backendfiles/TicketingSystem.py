from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from flask_cors import CORS
from requests.auth import HTTPBasicAuth
from EnDe import PasswordEncrypter

app = Flask(__name__)
CORS(app)


# MongoDB connection
client = MongoClient("mongodb+srv://net-bot:test123@cluster0.uuwhk.mongodb.net/")  
db = client['IntegrationSystem']  
collection = db['Integrations'] 

#Function to verify the JIRA credentials 
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

#Endpoint to authenticate jira credentials
@app.route('/jira/authenticate', methods=['POST'])
def jira_authenticate():
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

#Endpoint to save jira credentials
@app.route('/jira/save', methods=['POST'])
def jira_save_credentials():
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

#Endpoint to authenticate ServiceNow Credentials
@app.route('/ServiceNow/authenticate', methods=['POST'])
def serviceNow_authenticate():
    try:
        data = request.json
        instance_url = data.get("instance_url")
        username = data.get("username")
        password = data.get("password")

        if not instance_url or not username or not password:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Validate ServiceNow credentials
        api_url = f"{instance_url}/api/now/table/incident?sysparm_limit=1"
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Authenticated successfully"})
        elif response.status_code == 401:
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
        elif response.status_code == 404:
            return jsonify({"success": False, "message": "Invalid instance URL"}), 404
        else:
            return jsonify({"success": False, "message": f"Error: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

#Endpoint to save ServiceNow credentials
@app.route('/ServiceNow/save', methods=['POST'])
def serviceNow_save_credentials():
    try:
        data = request.json
        instance_url = data.get("instance_url")
        username = data.get("email")
        password = data.get("password")
        encrypted_ser_pass = PasswordEncrypter.encrypt_password(password)


        if not instance_url or not username or not password:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Save credentials in MongoDB
        collection.insert_one({
            "system": "ServiceNow",
            "instance_url": instance_url,
            "adminid": username,
            "password": encrypted_ser_pass,
        })

        return jsonify({"success": True, "message": "Credentials saved successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

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


# Endpoint to save data in  zendesk in MongoDB
@app.route('/zendesk/save', methods=['POST'])
def zendesk_save_data():
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
    app.run(debug=True, port=5102)