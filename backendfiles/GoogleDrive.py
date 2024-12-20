"""works for 7 file extensions - file getiing displayed in the terminal"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import pickle
import io
import tempfile
import subprocess
import platform
 
class GoogleDriveFileManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        self.creds = None
        self.service = None
   
    def authenticate(self):
        """Handle Google Drive authentication"""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
       
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
           
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
       
        self.service = build('drive', 'v3', credentials=self.creds)
   
    def search_file(self, query):
        """Search for files in Google Drive with various types including MP3 and MP4."""
        search_query = f"name contains '{query}' and (mimeType='application/pdf' or mimeType='image/jpeg' or mimeType='image/png' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType='application/msword' or mimeType='audio/mpeg' or mimeType='video/mp4' or mimeType = 'text/plain')"
       
        try:
            results = self.service.files().list(
                q=search_query,
                spaces='drive',
                fields='files(id, name, mimeType)',
                pageSize=10
            ).execute()
           
            return results.get('files', [])
        except Exception as e:
            print(f"Error while searching: {e}")
            return []
 
    def view_file(self, file_id, mime_type):
        """Get and view a file based on its mime type, now including MP3 and MP4."""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            done = False
           
            print("Fetching file...")
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
           
            # Create a temporary file based on the mime type
            suffix = ''
            if mime_type == 'application/pdf':
                suffix = '.pdf'
            elif mime_type == 'image/jpeg':
                suffix = '.jpg'
            elif mime_type == 'image/png':
                suffix = '.png'
            elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                suffix = '.docx' if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' else '.doc'
            elif mime_type == 'audio/mpeg':  
                suffix = '.mp3'
            elif mime_type == 'video/mp4':  
                suffix = '.mp4'
            elif mime_type == 'text/plain':  
                suffix = '.txt'    
           
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(file_io.getvalue())
                tmp_path = tmp_file.name
           
            # Open the file with the appropriate viewer
            self._open_file(tmp_path, mime_type)
           
        except Exception as e:
            print(f"Error while viewing file: {e}")
 
    def _open_file(self, file_path, mime_type):
        """Open the file with system default viewer based on the file type, including audio and video."""
        try:
            if mime_type == 'audio/mpeg':  # For MP3
                if platform.system() == 'Darwin':
                    subprocess.run(['open', file_path])
                elif platform.system() == 'Windows':
                    os.startfile(file_path)
                else:  # Linux
                    subprocess.run(['xdg-open', file_path])
            elif mime_type == 'video/mp4':  # For MP4
                if platform.system() == 'Darwin':
                    subprocess.run(['open', file_path])
                elif platform.system() == 'Windows':
                    os.startfile(file_path)
                else:  # Linux
                    subprocess.run(['xdg-open', file_path])
            elif mime_type == 'text/plain':  # For text files
                if platform.system() == 'Darwin':
                    subprocess.run(['open', file_path])
                elif platform.system() == 'Windows':
                    os.startfile(file_path)
                else:  # Linux
                    subprocess.run(['xdg-open', file_path])        
            else:
                # Existing logic for other file types
                if mime_type in ['application/pdf']:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', file_path])
                    elif platform.system() == 'Windows':
                        os.startfile(file_path)
                    else:  # Linux
                        subprocess.run(['xdg-open', file_path])
                elif mime_type in ['image/jpeg', 'image/png']:
                    # Open images
                    if platform.system() == 'Darwin':
                        subprocess.run(['open', file_path])
                    elif platform.system() == 'Windows':
                        os.startfile(file_path)
                    else:
                        subprocess.run(['xdg-open', file_path])
                elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                    # Open documents
                    if platform.system() == 'Darwin':
                        subprocess.run(['open', file_path])
                    elif platform.system() == 'Windows':
                        os.startfile(file_path)
                    else:
                        subprocess.run(['xdg-open', file_path])
        except Exception as e:
            print(f"Error opening file: {e}")
 
class DriveChatbot:
    def __init__(self):
        print("Initializing file viewer chatbot...")
        self.file_manager = GoogleDriveFileManager()
        self.file_manager.authenticate()
        print("Authentication successful!")
 
    def start(self):
        print("\nWelcome to file Viewer Chatbot!")
        print("You can search for files in your Google Drive and view them.")
        print("Type 'quit' to exit.")
       
        while True:
            query = input("\nWhich file would you like to search for? > ").strip()
           
            if query.lower() == 'quit':
                print("Goodbye!")
                break
           
            if not query:
                print("Please enter a search term.")
                continue
           
            results = self.file_manager.search_file(query)
           
            if not results:
                print("No such files found matching your search.")
                continue
           
            # Display results
            print("\nFound these files:")
            for i, file in enumerate(results, 1):
                print(f"{i}. {file['name']} (Type: {file['mimeType']})")
           
            # Get user choice
            while True:
                choice = input("\nEnter the number of the file you want to view (or 'back' to search again): ").strip()
               
                if choice.lower() == 'back':
                    break
               
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(results):
                        selected_file = results[choice_num - 1]
                        print(f"\nOpening '{selected_file['name']}'...")
                        self.file_manager.view_file(selected_file['id'], selected_file['mimeType'])
                        break
                    else:
                        print("Please enter a valid number from the list.")
                except ValueError:
                    print("Please enter a valid number or 'back'.")
 
def main():
    try:
        chatbot = DriveChatbot()
        chatbot.start()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
 
if __name__ == "__main__":
    main()
"""tts and ocr - ORIGINAL works in storing content in milvus """
