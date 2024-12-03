import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Static credentials
STATIC_USERNAME = "admin"
STATIC_PASSWORD = "@Shyam2610"

def validate_servicenow_instance(url):
    # Use the incident API as a check for ServiceNow instance validation
    api_url = f"{url}/api/now/table/incident"
    try:
        response = requests.get(api_url, auth=(STATIC_USERNAME, STATIC_PASSWORD), timeout=5)
        # If status code is 200, the URL is valid
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        # If there is a connection error or timeout
        return False

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Parse request JSON
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check static credentials
    if username == STATIC_USERNAME and password == STATIC_PASSWORD:
        return jsonify({"success": True, "message": "Authenticated successfully!"})
    return jsonify({"success": False, "message": "Invalid username or password."})

@app.route('/validate-url', methods=['POST'])
def validate_url():
    data = request.json
    instance_url = data.get("instance_url")
    
    # Validate the ServiceNow URL
    if validate_servicenow_instance(instance_url):
        return jsonify({"success": True, "message": "Valid ServiceNow instance!"})
    else:
        return jsonify({"success": False, "message": "Invalid ServiceNow instance URL."})

@app.route('/save', methods=['POST'])
def save():
    # Parse request JSON
    data = request.json
    system = data.get("system")
    instance_url = data.get("instance_url")

    # For now, just return success without saving to a database
    if system and instance_url:
        return jsonify({"success": True, "message": "Data saved successfully!"})
    return jsonify({"success": False, "message": "System or URL is missing."})

if __name__ == "__main__":
    app.run(debug=True)
