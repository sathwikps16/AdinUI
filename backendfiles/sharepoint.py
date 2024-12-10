# import msal
# import requests
# import os
# import webbrowser
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import urllib.parse
# from milvus_imple import MultiDepartmentVectorDB
# from dotenv import load_dotenv


# class SharePointApp:
#     def __init__(self):
#         # Load environment variables
#         load_dotenv()
#         self.client_id = os.getenv("CLIENT_ID")
#         self.client_secret = os.getenv("CLIENT_SECRET")
#         self.tenant_id = os.getenv("TENANT_ID")
#         self.site_url = os.getenv("SHAREPOINT_SITE_URL")  # SharePoint site URL from .env
#         self.library_name = os.getenv("SHAREPOINT_LIBRARY_NAME")  # Library name from .env
#         self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
#         self.scopes = ["https://graph.microsoft.com/.default"]
#         self.redirect_uri = "http://localhost:8000"

#         # Validate required environment variables
#         if not self.site_url:
#             raise ValueError("SHAREPOINT_SITE_URL is not set in the environment variables.")
#         if not self.library_name:
#             raise ValueError("SHAREPOINT_LIBRARY_NAME is not set in the environment variables.")

#         # Initialize MSAL application
#         self.app = msal.ConfidentialClientApplication(
#             self.client_id, authority=self.authority, client_credential=self.client_secret
#         )

#         self.access_token = None
#         self.vector_db = MultiDepartmentVectorDB()  # Milvus integration

#     def authenticate(self):
#         """Authenticate and retrieve access token."""
#         result = self.app.acquire_token_for_client(scopes=self.scopes)
#         if "access_token" in result:
#             self.access_token = result["access_token"]
#             print("Authentication successful!")
#             return True
#         else:
#             print("Authentication failed.")
#             print(result.get("error_description"))
#             return False

#     def get_headers(self):
#         """Get headers for SharePoint API requests."""
#         return {
#             "Authorization": f"Bearer {self.access_token}",
#             "Accept": "application/json",
#             "Content-Type": "application/json"
#         }

#     def get_site_id(self):
#         """Retrieve the site ID for the SharePoint site."""
#         url = f"https://graph.microsoft.com/v1.0/sites/{self.site_url}"
#         response = requests.get(url, headers=self.get_headers())
#         response.raise_for_status()
#         return response.json()["id"]

#     def list_files(self):
#         """List files in the SharePoint library."""
#         site_id = self.get_site_id()
#         url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/children"
#         response = requests.get(url, headers=self.get_headers())
#         response.raise_for_status()
#         return response.json().get("value", [])

#     def download_and_store_file(self, file_id, file_name, department, is_image=False):
#         """Download a file from SharePoint and store it in Milvus."""
#         site_id = self.get_site_id()
#         download_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}/content"
#         headers = self.get_headers()
#         response = requests.get(download_url, headers=headers, stream=True)
#         response.raise_for_status()

#         # Save the file temporarily
#         temp_folder = "temp_files"
#         os.makedirs(temp_folder, exist_ok=True)
#         temp_file_path = os.path.join(temp_folder, file_name)

#         with open(temp_file_path, "wb") as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 f.write(chunk)

#         print(f"File '{file_name}' downloaded successfully.")

#         # Upload to Milvus using MultiDepartmentVectorDB
#         success = self.vector_db.upload_file_to_department(
#             department=department, file_path=temp_file_path, is_image=is_image
#         )
#         if success:
#             print(f"File '{file_name}' stored in Milvus under {department} department.")
#         else:
#             print(f"Failed to store '{file_name}' in Milvus.")

#         # Clean up temporary file
#         os.remove(temp_file_path)

#     def download_file_by_name(self, file_name):
#         """Download a file by its name and ask for the department to upload."""
#         files = self.list_files()
#         for item in files:
#             if item.get("name") == file_name and "file" in item:
#                 department = input(
#                     "Enter the department to upload the file to (HR, IT, FINANCE, OTHERS): "
#                 ).upper()
#                 is_image = item["name"].lower().endswith((".png", ".jpg", ".jpeg"))
#                 self.download_and_store_file(
#                     file_id=item["id"],
#                     file_name=item["name"],
#                     department=department,
#                     is_image=is_image
#                 )
#                 return True

#         print(f"File '{file_name}' not found.")
#         return False


# def main():
#     app = SharePointApp()

#     if not app.authenticate():
#         return

#     print("\nListing files in SharePoint library...")
#     files = app.list_files()

#     print("\nFiles and Folders:")
#     print("-----------------")
#     for item in files:
#         if "folder" in item:
#             print(f"📁 {item['name']}")
#         elif "file" in item:
#             print(f"📄 {item['name']}")

#     file_name = input("\nEnter the name of the file to download: ")
#     if app.download_file_by_name(file_name):
#         print("Process completed. Exiting.")
#     else:
#         print("No files downloaded. Exiting.")


# if __name__ == "__main__":
#     main()
