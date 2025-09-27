import gspread
import json
import os
from google.oauth2.service_account import Credentials
from loguru import logger
from datetime import datetime


class SheetsClient:
    def __init__(self):
        self.client = None
        self._connect()

    def _connect(self):
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]

            # Попробуем загрузить credentials из переменной окружения или файла
            creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
            if creds_json:
                creds_dict = json.loads(creds_json)
                creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            else:
                creds = Credentials.from_service_account_file('credentials.json', scopes=scope)

            self.client = gspread.authorize(creds)
            logger.info("Connected to Google Sheets API")
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            self.client = None

    def get_all_data(self):
        if not self.client:
            logger.warning("No Google Sheets connection")
            return []

        try:
            sheet_url = 'https://docs.google.com/spreadsheets/d/1k4sQCH30fDpXKeO0mHbtzBHlKWvHAA5udyAzZXDBm5w'
            sheet_id = sheet_url.split('/')[5]
            spreadsheet = self.client.open_by_key(sheet_id)

            # try several worksheet names, fallback to first
            possible_names = ["Campaigns", "campaigns", "Campaign", "campaign", "Sheet1", "Лист1"]
            ws = None
            for name in possible_names:
                try:
                    ws = spreadsheet.worksheet(name)
                    logger.info(f"Found worksheet: {name}")
                    break
                except Exception:
                    continue
            if not ws:
                ws = spreadsheet.worksheets()[0]
                logger.info(f"Using first worksheet: {ws.title}")

            records = ws.get_all_records()
            logger.info(f"Loaded {len(records)} records from Google Sheets")
            return records

        except Exception as e:
            logger.error(f"Error reading from Google Sheets: {e}")
            return []

    def check_dash_code_exists(self, dash_code):
        data = self.get_all_data()

        try:
            dash_code_int = int(dash_code)
        except Exception:
            logger.warning(f"Invalid dash code format: {dash_code}")
            return False

        dash_codes = []
        for row in data:
            if not isinstance(row, dict):
                continue
            val = row.get('Dash_Code') or row.get('Dash Code') or row.get('dash_code')
            if val is None:
                continue
            # normalize numeric-like values
            try:
                if isinstance(val, (int, float)):
                    dash_codes.append(int(val))
                else:
                    s = str(val).strip()
                    # extract digits in case of formatting
                    digits = ''.join(ch for ch in s if ch.isdigit())
                    if digits:
                        dash_codes.append(int(digits))
            except Exception:
                continue

        exists = dash_code_int in dash_codes
        logger.info(f"Checking code {dash_code} : {'found' if exists else 'not found'}")
        return exists

    def get_campaigns_by_code(self, dash_code):
        data = self.get_all_data()

        try:
            dash_code_int = int(dash_code)
        except Exception:
            return []

        campaigns = []
        for row in data:
            if not isinstance(row, dict):
                continue
            val = row.get('Dash_Code') or row.get('Dash Code') or row.get('dash_code')
            if val is None:
                continue
            try:
                if isinstance(val, (int, float)) and int(val) == dash_code_int:
                    campaigns.append(row)
                else:
                    s = str(val).strip()
                    digits = ''.join(ch for ch in s if ch.isdigit())
                    if digits and int(digits) == dash_code_int:
                        campaigns.append(row)
            except Exception:
                continue

        logger.info(f"Found {len(campaigns)} campaigns for code {dash_code}")
        return campaigns

    def get_users_sheet(self):
        try:
            sheet_url = "https://docs.google.com/spreadsheets/d/1k4sQCH30fDpXKeO0mHbtzBHlKWvHAA5udyAzZXDBm5w"
            sheet_id = sheet_url.split('/')[5]
            spreadsheet = self.client.open_by_key(sheet_id)

            # try to find Users sheet by several names
            possible_names = ["Users", "users", "User", "user", "Sheet2", "Лист2"]
            ws = None
            for name in possible_names:
                try:
                    ws = spreadsheet.worksheet(name)
                    logger.info(f"Found users worksheet with name: {name}")
                    break
                except Exception:
                    continue

            if not ws:
                # fallback to second worksheet if exists, otherwise create
                worksheets = spreadsheet.worksheets()
                if len(worksheets) > 1:
                    ws = worksheets[1]
                    logger.info(f"Using second worksheet as users: {ws.title}")
                else:
                    ws = spreadsheet.add_worksheet(title="Users", rows="100", cols="20")
                    logger.info("Created new Users worksheet")

            return ws

        except Exception as e:
            logger.error(f"Error accessing Users sheet: {e}")
            return None

    def save_user_to_sheets(self, client_id, telegram_id, first_name, username):
        try:
            users_worksheet = self.get_users_sheet()
            if not users_worksheet:
                logger.error("API connection error,users sheet not accessible")
                return False

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            if self.check_user_exists_in_sheets(telegram_id):
                logger.info(f"User {telegram_id} already exists")
                return True

            # append row in correct order
            users_worksheet.append_row([client_id, telegram_id, first_name, username, timestamp])
            logger.info(f"User {telegram_id} saved successfully")
            return True

        except Exception as e:
            logger.error(f"Error saving user to sheets: {e}")
            return False

    def get_user_from_sheets(self, telegram_id):
        try:
            users_sheet = self.get_users_sheet()
            if not users_sheet:
                return None

            records = users_sheet.get_all_records()

            for record in records:
                # check several possible column names
                if record.get('telegram_id') == telegram_id or record.get('Telegram ID') == telegram_id or str(
                        record.get('Telegram_ID')) == str(telegram_id):
                    return record.get('client_id') or record.get('Client ID')

            return None

        except Exception as e:
            logger.error(f"Error getting user from sheets: {e}")
            return None

    def check_user_exists_in_sheets(self, telegram_id):
        try:
            return self.get_user_from_sheets(telegram_id) is not None
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")
            return False


sheets_client = SheetsClient()
