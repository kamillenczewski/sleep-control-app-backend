from google.oauth2 import service_account
from googleapiclient.discovery import build
from secret_loader import SecretLoader
from json import loads

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SPREADSHEET_ID = "1l7fnFTegPB-q481cXsj8kNhr6XYRFgyAH27ik5OmB7E"
SPREADSHEET_ID = "1_xMafoiaDvKoJeACF9MuQkunGkFOpr8jUIUFXH75y8Y"
KEY = loads(SecretLoader.get('GOOGLE_SERVICE_ACCOUNT_KEY').replace("\\n", "\n"))

creds = service_account.Credentials.from_service_account_info(
    KEY, 
    scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)

sheet = service.spreadsheets()

def get(range):
    return sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range
    ).execute().get('values', [])