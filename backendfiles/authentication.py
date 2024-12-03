from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
import requests
import sqlite3

app = Flask(__name__)
CORS(app)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = '1234'  
jwt = JWTManager(app)

# Database setup
def init_db():
    conn = sqlite3.connect('ticketing_connections.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS connections
                 (id INTEGER PRIMARY KEY, 
                  system TEXT, 
                  instance_url TEXT, 
                  username TEXT, 
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Authentication validator for ServiceNow
def validate_servicenow_credentials(username, password):
    try:
        api_url = "https://dev261475.service-now.com/api/now/table/incident"
        response = requests.get(api_url, auth=(username, password), timeout=10)
        if response.status_code == 200:
            return True, [{"name": "Production Instance", "url": "https://dev261475.service-now.com"}]
        elif response.status_code == 401:
            return False, "Invalid ServiceNow credentials"
        else:
            return False, f"ServiceNow responded with status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Error connecting to ServiceNow: {e}"

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    system = data.get("system")
    username = data.get("username")
    password = data.get("password")

    if not all([system, username, password]):
        return jsonify({"success": False, "message": "Missing system, username, or password"}), 400

    if system != "ServiceNow":
        return jsonify({"success": False, "message": "Unsupported ticketing system"}), 400

    is_valid, message_or_instances = validate_servicenow_credentials(username, password)
    if is_valid:
        access_token = create_access_token(identity=username)
        return jsonify({
            "success": True,
            "message": "Authentication successful",
            "token": access_token,
            "instances": message_or_instances
        }), 200

    return jsonify({"success": False, "message": message_or_instances}), 401

@app.route('/save', methods=['POST'])
@jwt_required()
def save():
    data = request.json
    instance_url = data.get("instance_url")
    system = data.get("system")
    username = get_jwt_identity()

    if not all([instance_url, system]):
        return jsonify({"success": False, "message": "Missing instance URL or system"}), 400

    conn = sqlite3.connect('ticketing_connections.db')
    c = conn.cursor()
    c.execute("INSERT INTO connections (system, instance_url, username) VALUES (?, ?, ?)",
              (system, instance_url, username))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Data saved successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
