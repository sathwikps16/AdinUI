from flask import Flask, request, jsonify
from pymongo import MongoClient
from requests.auth import HTTPBasicAuth
from flask_cors import CORS
import requests
from EnDe import PasswordEncrypter

app = Flask(__name__)
CORS(app)

# MongoDB configuration
client = MongoClient("mongodb+srv://net-bot:test123@cluster0.uuwhk.mongodb.net/")
db = client['TicketingSystemDB']
collection = db['TicketingSystem']

@app.route('/authenticate', methods=['POST'])
def authenticate():
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

@app.route('/save', methods=['POST'])
def save_credentials():
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

if __name__ == "__main__":
    app.run(port=5106, debug=True)
