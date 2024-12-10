import requests
from requests.auth import HTTPBasicAuth

def validate_servicenow_credentials(instance_url, username, password):
    try:
        # API endpoint for checking instance
        api_url = f"{instance_url}/api/now/table/incident?sysparm_limit=1"
        
        # Send a GET request with basic authentication
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
        
        # Check if the response indicates a successful authentication
        if response.status_code == 200:
            print("ServiceNow credentials are valid.")
            return True
        elif response.status_code == 401:
            print("Invalid username or password.")
            return False
        elif response.status_code == 404:
            print("Invalid ServiceNow instance URL.")
            return False
        else:
            print(f"Failed to validate credentials. HTTP Status Code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to ServiceNow: {e}")
        return False

# Your ServiceNow credentials
instance_url = "https://dev291644.service-now.com"
username = "admin"
password = "56O$emVsZqA%"

# Validate the credentials
validate_servicenow_credentials(instance_url, username, password)
