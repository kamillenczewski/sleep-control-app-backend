from google.oauth2 import service_account
from googleapiclient.discovery import build
from tools import getSecret

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1l7fnFTegPB-q481cXsj8kNhr6XYRFgyAH27ik5OmB7E"

creds = service_account.Credentials.from_service_account_info(
    getSecret('GOOGLE_SERVICE_ACCOUNT_KEY'), 
    scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)

sheet = service.spreadsheets()

def get(range):
    return sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range
    ).execute().get('values', [])