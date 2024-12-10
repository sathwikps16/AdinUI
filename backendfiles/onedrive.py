# onedrive.py
import msal
import requests
import os
from dotenv import load_dotenv
from milvus_imple import MultiDepartmentVectorDB

class OneDriveHandler:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tenant_id = os.getenv("TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scopes = [
            "https://graph.microsoft.com/Files.ReadWrite.All",
            "https://graph.microsoft.com/Files.Read.All",
            "https://graph.microsoft.com/Files.Read"
        ]
        self.app = msal.ConfidentialClientApplication(
            self.client_id, authority=self.authority, client_credential=self.client_secret
        )
        self.access_token = None
        self.vector_db = MultiDepartmentVectorDB()

    def get_token(self):
        """Retrieve a token using client credentials."""
        result = self.app.acquire_token_for_client(scopes=self.scopes)
        if "access_token" in result:
            self.access_token = result["access_token"]
            return True
        return False

    def list_files(self):
        """List files in the OneDrive root folder."""
        url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])

    def download_and_store_file(self, file_id, file_name, department, is_image=False):
        """Download and store the file in Milvus."""
        download_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(download_url, headers=headers, stream=True)
        response.raise_for_status()

        temp_file_path = os.path.join("temp_files", file_name)
        os.makedirs("temp_files", exist_ok=True)
        with open(temp_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        success = self.vector_db.upload_file_to_department(
            department=department, file_path=temp_file_path, is_image=is_image
        )
        os.remove(temp_file_path)
        return success

    def download_file_by_name(self, file_name, department):
        """Find a file by name and upload to Milvus."""
        files = self.list_files()
        for item in files:
            if item.get("name") == file_name and "file" in item:
                is_image = file_name.lower().endswith((".png", ".jpg", ".jpeg"))
                return self.download_and_store_file(
                    file_id=item["id"],
                    file_name=file_name,
                    department=department,
                    is_image=is_image
                )
        return False
