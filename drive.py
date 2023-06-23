import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from tqdm import tqdm

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/workspaces/ag-data/creds.json'

# Set the ID of the destination folder in Google Drive
DESTINATION_FOLDER_ID = '1rjAf8RuQdQ6TiIFkh_D7OEaltZbIXHOQ'

def upload_folder_to_drive(service, folder_path, parent_folder_id):
    folder_name = os.path.basename(folder_path)

    # Create a folder in Google Drive
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')

    # Upload files in the folder
    for file_name in tqdm(os.listdir(folder_path), desc = f"Uploading {folder_name}"):
        try:
            # print(f'Uploading {file_name}')
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(file_path)
                service.files().create(body=file_metadata, media_body=media).execute()
            elif os.path.isdir(file_path):
                upload_folder_to_drive(service, file_path, folder_id)
        except:
            print(f"failed uploading {folder_name}/{file_name}")
            continue

    # print(f'◤ Folder "{folder_name}" uploaded to Google Drive. ◢')

def get_newest_folder(path):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    newest_folder = max(folders, key=lambda f: os.path.getctime(os.path.join(path, f)))
    return newest_folder

def main():
    # Build the Google Drive API service
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    # for x in FOLDER_PATHS:
    #     upload_folder_to_drive(service, x, DESTINATION_FOLDER_ID)

    # folder_path = 
    newest_folder = f"/workspaces/ag-data/extract/{get_newest_folder('/workspaces/ag-data/extract/')}"
    # print("Newest folder:", newest_folder)

    upload_folder_to_drive(service, newest_folder, DESTINATION_FOLDER_ID)

if __name__ == '__main__':
    main()
