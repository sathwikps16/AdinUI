# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# import imaplib
# from flask_cors import CORS
# from EnDe import PasswordEncrypter

# app = Flask(__name__)
# CORS(app)

# client = MongoClient("mongodb+srv://net-bot:test123@cluster0.uuwhk.mongodb.net/")
# db = client['IntegrationSystem']
# collection = db['Integrations']

# def validate_imap_credentials(email, app_password, server, port):
#     try:
#         mail = imaplib.IMAP4_SSL(server, port)
#         mail.login(email, app_password)
#         print("Authentication successful!")
#         return True, "Authentication successful."  

#     except imaplib.IMAP4.error:
#         print("Authentication failed. Please check your credentials.")
#         return False, "Authentication failed. Please check your credentials."  

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return False, f"An error occurred: {e}"

#     finally:
#         try:
#             mail.logout()
#         except:
#             pass

# @app.route('/api/verify-imap', methods=['POST'])
# def verify_smtp():
#     data = request.json
#     shared_email = data.get('sharedEmail')   
#     app_password = data.get('appPassword')
#     port_number = data.get('portNumber', 993)
#     imap_server = data.get('imapServer')

#     if not shared_email or not app_password or not port_number or not imap_server:
#         return jsonify({"success": False, "message": "All fields are required."}), 400

#     is_valid, message = validate_imap_credentials(shared_email, app_password, imap_server, port_number)

#     if is_valid:
#         return jsonify({"success": True, "message": message}), 200
#     else:
#         return jsonify({"success": False, "message": message}), 400

# @app.route('/api/save-shared-email', methods=['POST'])
# def save_shared_email():
#     data = request.json
#     shared_email = data.get('sharedEmail')
#     port_number = data.get('portNumber')
#     app_password = data.get('appPassword')
#     imap_server = data.get('imapServer')

#     if not shared_email or not port_number or not app_password or not imap_server:
#         return jsonify({"success": False, "message": "All fields are required."}), 400

#     try:
#         encrypted_app_password = PasswordEncrypter.encrypt_password(app_password)
#         collection.insert_one({
#             "sharedEmail": shared_email,
#             "Port Number": port_number,
#             "IMAP Server": imap_server,
#             "App Password": encrypted_app_password
#         })
#         return jsonify({"success": True, "message": "Credentials saved successfully."}), 200
#     except Exception as e:
#         return jsonify({"success": False, "message": f"Failed to save credentials: {e}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5104)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


from flask import Flask, request, jsonify
from pymongo import MongoClient
import imaplib
from socket import timeout
from flask_cors import CORS
from EnDe import PasswordEncrypter

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://net-bot:test123@cluster0.uuwhk.mongodb.net/")
db = client['IntegrationSystem']
collection = db['Integrations']

def validate_imap_credentials(email, app_password, server, port):
    try:
        mail = imaplib.IMAP4_SSL(server, port, timeout=10)  # 10 seconds timeout
        mail.login(email, app_password)
        print("Authentication successful!")
        return True, "Authentication successful."  

    except timeout:
        print("Connection timed out. Please check the server and port number.")
        return False, "Connection timed out. Please check the server and port number."

    except imaplib.IMAP4.error:
        print("Authentication failed. Please check your credentials.")
        return False, "Authentication failed. Please check your credentials."  

    except Exception as e:
        print(f"An error occurred: {e}")
        return False, f"An error occurred: {e}"

    finally:
        try:
            mail.logout()
        except:
            pass

@app.route('/api/verify-imap', methods=['POST'])
def verify_smtp():
    data = request.json
    shared_email = data.get('sharedEmail')   
    app_password = data.get('appPassword')
    port_number = data.get('portNumber', 993)
    imap_server = data.get('imapServer')

    if not shared_email or not app_password or not port_number or not imap_server:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        port_number = int(port_number)
    except ValueError:
        return jsonify({"success": False, "message": "Port number must be an integer."}), 400

    is_valid, message = validate_imap_credentials(shared_email, app_password, imap_server, port_number)

    if is_valid:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400

@app.route('/api/save-shared-email', methods=['POST'])
def save_shared_email():
    data = request.json
    shared_email = data.get('sharedEmail')
    port_number = data.get('portNumber')
    app_password = data.get('appPassword')
    imap_server = data.get('imapServer')

    if not shared_email or not port_number or not app_password or not imap_server:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        encrypted_app_password = PasswordEncrypter.encrypt_password(app_password)
        collection.insert_one({
            "sharedEmail": shared_email,
            "Port Number": port_number,
            "IMAP Server": imap_server,
            "App Password": encrypted_app_password
        })
        return jsonify({"success": True, "message": "Credentials saved successfully."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to save credentials: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5104)
