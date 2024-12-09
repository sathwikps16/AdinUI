import msal
import requests
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from milvus_imple import MultiDepartmentVectorDB
from dotenv import load_dotenv

class AuthCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle the authorization code callback"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Parse the authorization code from URL
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Store the auth code in server's auth_code attribute
        if "code" in query_components:
            self.server.auth_code = query_components["code"][0]

        # Display success message with auto-close script
        self.wfile.write(b"""
        <html>
        <head>
            <title>Authentication Successful</title>
            <script>                
                setTimeout(() => window.close(), 100);
            </script>
        </head>
        <body>
            <h1>Authentication successful!</h1>
            <p>You can close this window or it will close automatically.</p>
        </body>
        </html>
        """)


class OneDriveConsoleApp:
    def __init__(self):
        # OneDrive App details
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tenant_id = os.getenv("TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scopes = [
            "https://graph.microsoft.com/Files.ReadWrite.All",
            "https://graph.microsoft.com/Files.Read.All",
        ]
        self.redirect_uri = "http://localhost:8000"

        # Initialize MSAL application
        self.app = msal.ConfidentialClientApplication(
            self.client_id, authority=self.authority, client_credential=self.client_secret
        )

        # Token cache
        self.cached_token = None
        self.access_token = None

        # Initialize Milvus database handler
        self.vector_db = MultiDepartmentVectorDB() 

    def get_cached_token(self):
        """Retrieve token from in-memory cache."""
        return self.cached_token

    def save_token_to_cache(self, token):
        """Save token to in-memory cache."""
        self.cached_token = token

    def get_token(self):
        """Retrieve token, refreshing or authenticating as necessary."""
        cached_token = self.get_cached_token()
        if cached_token and "access_token" in cached_token:
            if self.is_token_valid(cached_token):
                print("Using cached token")
                self.access_token = cached_token["access_token"]
                return True

        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
            if "access_token" in result:
                self.save_token_to_cache(result)
                self.access_token = result["access_token"]
                print("Token refreshed successfully.")
                return True

        return self.authenticate_interactively()

    def is_token_valid(self, token):
        """Check if a token is still valid based on expiration time."""
        import time
        return time.time() < token.get("expires_at", 0)

    def authenticate_interactively(self):
        """Perform interactive authentication."""
        server = HTTPServer(("localhost", 8000), AuthCodeHandler)
        server.auth_code = None

        auth_url = self.app.get_authorization_request_url(
            scopes=self.scopes, redirect_uri=self.redirect_uri
        )
        # print("Opening browser for authentication...")
        webbrowser.open(auth_url)

        while server.auth_code is None:
            server.handle_request()

        result = self.app.acquire_token_by_authorization_code(
            code=server.auth_code, scopes=self.scopes, redirect_uri=self.redirect_uri
        )
        if "access_token" in result:
            self.save_token_to_cache(result)
            self.access_token = result["access_token"]
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed.")
            return False

    def list_files(self, item_id=None):
        """List files in OneDrive root or specified folder."""
        url = (
            f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/children"
            if item_id
            else "https://graph.microsoft.com/v1.0/me/drive/root/children"
        )
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            print("Token expired. Refreshing token...")
            self.get_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json().get("value", [])
    
    def download_and_store_file(self, file_id, file_name, department, is_image=False):
        """Download a file and store it in Milvus."""
        download_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(download_url, headers=headers, stream=True)
        response.raise_for_status()

        # Save the file temporarily
        temp_folder = "temp_files"
        os.makedirs(temp_folder, exist_ok=True)
        temp_file_path = os.path.join(temp_folder, file_name)

        with open(temp_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File '{file_name}' downloaded successfully.")

        # Upload to Milvus using MultiDepartmentVectorDB
        success = self.vector_db.upload_file_to_department(
            department=department, file_path=temp_file_path, is_image=is_image
        )
        if success:
            print(f"File '{file_name}' stored in Milvus under {department} department.")
        else:
            print(f"Failed to store '{file_name}' in Milvus.")
        # Clean up temporary file
        os.remove(temp_file_path)

    def download_file_by_name(self, file_name):
        """Download a file by its name and ask for the department to upload."""
        root_items = self.list_files()
        for item in root_items:
            if item.get("name") == file_name and "file" in item:
                # Prompt user for department
                department = input(
                    "Enter the department to upload the file to (HR, IT, FINANCE, OTHERS): "
                ).upper()

                # Check if the selected file is an image
                is_image = item["name"].lower().endswith((".png", ".jpg", ".jpeg"))

                # Download and store file in Milvus
                self.download_and_store_file(
                    file_id=item["id"], 
                    file_name=item["name"], 
                    department=department, 
                    is_image=is_image
                )
                return True

        print(f"File '{file_name}' not found.")
        return False

def main():
    app = OneDriveConsoleApp()

    if not app.get_token():
        return

    print("\nListing files in OneDrive root...")
    files = app.list_files()

    print("\nFiles and Folders:")
    print("-----------------")
    for item in files:
        if "folder" in item:
            print(f"📁 {item['name']}")
        elif "file" in item:
            print(f"📄 {item['name']}")

    file_name = input("\nEnter the name of the file to download: ")
    if app.download_file_by_name(file_name):
        print("Process completed. Exiting.")
    else:
        print("No files downloaded. Exiting.")

if __name__ == "__main__":
    main()
