from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
import requests
import mysql.connector
from PasswordEncrypter import PasswordEncrypter

app = Flask(__name__)
CORS(app)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = '1234'
jwt = JWTManager(app)

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="10.1.7.137",
        user="bhuvan",
        password="1234",
        database="ticketing_system_db"
    )

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    instance_url = data.get("instanceUrl")
    username = data.get("username")
    password = data.get("password")

    if not all([instance_url, username, password]):
        return jsonify({"success": False, "message": "Missing instance URL, username, or password"}), 400

    try:
        response = requests.get(f"{instance_url}/api/now/table/incident", auth=(username, password), timeout=10)
        if response.status_code == 200:
            access_token = create_access_token(identity=username)
            return jsonify({
                "success": True,
                "message": "Authentication successful",
                "token": access_token,
                "password": password  # Sent back for frontend use
            }), 200
        elif response.status_code == 401:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
        else:
            return jsonify({"success": False, "message": f"ServiceNow responded with status code {response.status_code}"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": f"Error connecting to ServiceNow: {e}"}), 500

@app.route('/save', methods=['POST'])
@jwt_required()
def save():
    data = request.json
    instance_url = data.get("instance_url")
    system = data.get("system")
    username = get_jwt_identity()
    password = data.get("password")  
    hash_password = PasswordEncrypter.hash_password(password)

    if not all([instance_url, system, password]):
        return jsonify({"success": False, "message": "Missing instance URL, system, or password"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Ticketing_System (Service_name, Instance_URL, Admin_ID, Password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (system, instance_url, username, hash_password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Data saved successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": f"Database error: {err}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
