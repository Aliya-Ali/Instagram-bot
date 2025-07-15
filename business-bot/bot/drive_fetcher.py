from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import io
from googleapiclient.http import MediaIoBaseDownload

# Authenticate using service account credentials
def authenticate_drive():
    creds = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build('drive', 'v3', credentials=creds)
    return service

# Download all images from a specific Google Drive folder
def download_all_images(service, folder_id, download_folder="images"):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print("No images found in the folder.")
        return []

    downloaded_files = []

    for file in items:
        file_id = file['id']
        file_name = file['name']
        file_path = os.path.join(download_folder, file_name)

        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()

        print(f"✅ Downloaded: {file_name}")
        downloaded_files.append(file_path)

    print(f"\n🎉 Total images downloaded: {len(downloaded_files)}")
    return downloaded_files
