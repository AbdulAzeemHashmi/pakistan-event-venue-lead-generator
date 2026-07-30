import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from config import Config

logger = logging.getLogger(__name__)

class SheetHandler:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        # Place service_account.json in project root
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(Config.SPREADSHEET_ID).worksheet(Config.SHEET_NAME)
        self.column_count = len(Config.COLUMNS)

    def get_existing_names(self):
        """Return all non-empty names from column A (index 1)."""
        all_values = self.sheet.col_values(1)  # column A
        # Skip header if present
        if all_values and all_values[0].lower() == "name":
            all_values = all_values[1:]
        return [v.strip() for v in all_values if v.strip()]

    def append_row(self, row_data):
        """Append a row to the sheet."""
        if len(row_data) < self.column_count:
            row_data += [""] * (self.column_count - len(row_data))
        elif len(row_data) > self.column_count:
            row_data = row_data[:self.column_count]
        self.sheet.append_row(row_data, value_input_option="USER_ENTERED")