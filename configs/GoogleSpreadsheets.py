# data loader for establishing connectivity to google spreadsheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from cryptography.fernet import Fernet

fernet_key_file = open('./fernet_key.key', 'rb')
fernet_key = fernet_key_file.read() # The key will be type bytes
fernet_key_file.close()

google_drive_api_key_file = open('./google_drive_api.key', 'rb')
google_drive_api_key = google_drive_api_key_file.read()
google_drive_api_key_file.close()

fernet = Fernet(fernet_key)
google_drive_api_key = json.loads(fernet.decrypt(google_drive_api_key).decode())

google_scope = ['https://www.googleapis.com/auth/drive']
google_creds = ServiceAccountCredentials.from_json_keyfile_dict(google_drive_api_key, google_scope)
google_client = gspread.authorize(google_creds)

def get_feedback_table_columns():
    return google_client.open("KelownaCommunityFeedback").sheet1.get_all_values()[0][:13]

def get_feedback_table_data():
    return google_client.open("KelownaCommunityFeedback").sheet1.get_all_records()
