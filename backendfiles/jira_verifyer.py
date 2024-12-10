import requests
from pymongo import MongoClient
from requests.auth import HTTPBasicAuth

def verify_jira_credentials(JIRA_URL, JIRA_USER, JIRA_API_TOKEN):
    """
    Verify the Jira credentials by checking if the user can authenticate with the Jira API.

    Args:
        JIRA_URL (str): The URL of the Jira instance.
        JIRA_USER (str): The Jira user's email or username.
        JIRA_API_TOKEN (str): The Jira API token for the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
        dict: User data if credentials are valid, else an error message.
    """
    # Jira API endpoint to check user information (using 'myself' endpoint)
    url = f"{JIRA_URL}/rest/api/2/myself"
    
    # Perform GET request to verify credentials
    try:
        response = requests.get(url, auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN))
        if response.status_code == 200:
            # Credentials are valid, return the user data
            user_data = response.json()
            return True, user_data
        else:
            # Invalid credentials
            return False, f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Exception occurred while connecting to Jira: {e}"



# Example usage:
JIRA_URL = "https://sushmaravishankar.atlassian.net/"  # Replace with your Jira instance URL
JIRA_USER = "priyankamcpriiya@gmail.com"  # Replace with your Jira email or username
JIRA_API_TOKEN = "ATATT3xFfGF0p8KmaWq-sDmVlzZkXxA4HXXgw5lgv_3yDzMuXp1pzmvIvWfwh28zRErDDQCvprmeEHj2wAMfhcIiKIAOdvxCsFyAlyoYoeP-hiFVrm6pb8M4pMC8TS-RZCrHmQMYfJvxrS-R96AfAp6iwXEdraFpEOVLZH2r2wpyAYGOQ_bNGe0=0A194C7D"  # Replace with your Jira API token

# Step 1: Verify Jira credentials
is_valid, result = verify_jira_credentials(JIRA_URL, JIRA_USER, JIRA_API_TOKEN)

if is_valid:
    print("Credentials are verified ")
else:
    print(f"Invalid Jira credentials: {result}")
