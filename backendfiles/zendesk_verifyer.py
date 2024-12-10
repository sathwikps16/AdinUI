# import requests
# from pymongo import MongoClient
# from requests.auth import HTTPBasicAuth

# # MongoDB Connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client['zendesk_db']
# collection = db['zendesk_credentials']

# def verify_zendesk_credentials(instance_url, admin_id, password):
#     """
#     Verifies Zendesk credentials by making a request to the Zendesk API.
#     Ensures the credentials provided match a valid user in the system.
#     """
#     # Build the API URL (e.g., "https://your_zendesk_instance.zendesk.com/api/v2/users/me.json")
#     url = f"{instance_url}/api/v2/users/me.json"
    
#     # Authenticate using basic authentication (admin_id as the email, password as the password)
#     auth = HTTPBasicAuth(admin_id, password)
    
#     try:
#         # Make a GET request to the Zendesk API
#         response = requests.get(url, auth=auth)
        
#         # Check if status code is 200 (success)
#         if response.status_code == 200:
#             user_data = response.json()  # Parse the JSON response

#             # Check if the 'user' object exists and the email matches the provided admin_id
#             if 'user' in user_data and user_data['user'].get('email') == admin_id:
#                 return True, "Credentials verified"
#             else:
#                 return False, "Invalid credentials: User email mismatch"

#         # If status code is 401, invalid credentials (wrong username/password)
#         elif response.status_code == 401:
#             return False, "Invalid credentials: Unauthorized access. Check your username or password."

#         # Handle other errors like 403, 404, etc.
#         else:
#             return False, f"Error: {response.status_code} - {response.text}"

#     except requests.exceptions.RequestException as e:
#         return False, f"Error connecting to Zendesk: {str(e)}"

# # Example usage:
# instance_url = "https://netanalytiks8569.zendesk.com"  # Replace with your Zendesk instance URL
# admin_id = "bhuvans@netanalytiks.com"  # Replace with your admin email
# password = "pulsar65653"  # Use incorrect password for testing

# is_valid, message = verify_zendesk_credentials(instance_url, admin_id, password)

# print(message)

import requests

def verify_zendesk_account_owner(instance_url, admin_email, api_token):
    url = f"{instance_url}/api/v2/users/me.json"  # Endpoint to get user data
    headers = {
        "Accept": "application/json"
    }

    # Basic Authentication with email and API token
    response = requests.get(url, auth=(f"{admin_email}/token", api_token), headers=headers)
    
    if response.status_code == 200:
        user_data = response.json().get('user', {})
        
        # Log the full user data to check roles and other details
        print(f"Full User Data: {user_data}")
        
        # Check if the role is account owner
        role = user_data.get('role', 'unknown')
        if role == 'admin':
            print("Account admin credentials are valid.")
            return True
        else:
            print(f"User role is not admin Role: {role}")
            return False
    elif response.status_code == 401:
        print("Unauthorized: Invalid email or API token.")
        return False
    else:
        print(f"Unexpected error: {response.status_code} - {response.text}")
        return False

# Example usage
instance_url = "https://netanalytiks8569.zendesk.com"
admin_email = "bhuvans@netanalytiks.com"  # Your admin email
api_token = "HbPWCA9S4a9psC4cop0S7aU9xHg9sRfrm292EJQy"  # Your API token

verify_zendesk_account_owner(instance_url, admin_email, api_token)
