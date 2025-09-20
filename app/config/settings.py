import os
from dotenv import load_dotenv

load_dotenv()

#Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ENVIRONMENT = os.getenv("ENVIRONMENT", "developement")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")
GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL")
GOOGLE_CREDENTIALS_PATH = "credentials.json"

