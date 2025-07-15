import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
load_dotenv()

def create_keyfile_dict():
    
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("❌ PRIVATE_KEY not found in environment variables")

    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": private_key.replace("\\n", "\n"),  # decode newlines
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    }



# Connect to Google Sheets
def connect_to_sheet(sheet_name: str):
    print(create_keyfile_dict())
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # Connect to first sheet
    return sheet



# Update status and profile link after submission
def update_submission( sheet, row_number, profile_link):
    sheet.update_cell(row_number, 4, profile_link) 

def get_vertical_business_data(sheet):
    """
    Reads key-value business data from column A and B only (ignoring others).
    """
    rows = sheet.get_all_values()
    data = {}

    for row in rows:
        if len(row) >= 2:
            key = row[0].strip()  # Column A
            value = row[1].strip()  # Column B
            if key and value:
                data[key] = value

    return data

