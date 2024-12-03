from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import set_key, load_dotenv
import os
 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
 
# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/ticketing_system_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialize the SQLAlchemy object
db = SQLAlchemy(app)
 
# Define the TicketingSystem model
class TicketingSystem(db.Model):
    __tablename__ = 'Ticketing_System'
 
    idTicketing_System = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(100), nullable=False, unique=True)
    instance_url = db.Column(db.String(500), nullable=False)
 
    def __repr__(self):
        return f"<TicketingSystem {self.service_name}>"
 
# Function to update the .env file
def update_env_file(service_name, instance_url):
    env_path = ".env"  # Ensure this points to your actual .env file location
    load_dotenv(env_path)
 
    # Update or create environment variables
    set_key(env_path, "SERVICE_NAME", service_name)
    set_key(env_path, "INSTANCE_URL", instance_url)
 
# Route to add or update a ticketing system
@app.route('/ticketing-system', methods=['POST'])
def add_or_update_ticketing_system():
    data = request.json
 
    # Get data from the request
    service_name = data.get('Service_name')
    instance_url = data.get('Instance_URL')
 
    # Validate the input
    if not service_name or not instance_url:
        return jsonify({"message": "Both Service_name and Instance_URL are required!"}), 400
 
    # Check if the ticketing system already exists
    ticketing_system = TicketingSystem.query.filter_by(service_name=service_name).first()
 
    if ticketing_system:
        # If exists, update the instance_url
        ticketing_system.instance_url = instance_url
    else:
        # If doesn't exist, create a new ticketing system entry
        ticketing_system = TicketingSystem(service_name=service_name, instance_url=instance_url)
        db.session.add(ticketing_system)
 
    try:
        # Commit to save the data
        db.session.commit()

        # Manually update the .env file
        update_env_file(service_name, instance_url)

        return jsonify({"message": "Ticketing system added/updated successfully"}), 200
    except Exception as e:
        # Handle errors, e.g., if the data violates unique constraints
        db.session.rollback()
        return jsonify({"message": "Error adding/updating ticketing system", "error": str(e)}), 500
 
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
