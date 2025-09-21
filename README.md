# PostAd Dashboard Bot

Telegram bot for viewing campaign statistics from Google Sheets dashboard.

## Features

- User registration with dashboard codes
- Campaign statistics display
- Google Sheets integration
- Command menu support
- Clickable campaign links

## Commands

- `/start` - Register with dashboard code
- `/stats` - View campaign statistics

## Setup

### Prerequisites

- Python 3.11+
- Google Cloud Service Account
- Telegram Bot Token
- Railway Account (for deployment)

### Environment Variables

Create these environment variables in Railway:

```
BOT_TOKEN=your_telegram_bot_token
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/your_sheet_id
ENVIRONMENT=production
DEBUG=false
```

### Google Sheets Structure

The bot expects these columns in your Google Sheet:

**Campaigns Sheet:**
- Campaign ID
- Dash_Code
- Company Name
- Cost
- Views
- CPM
- Date
- Campaign URL

**Users Sheet (auto-created):**
- client_id
- telegram_id
- first_name
- username
- timestamp

### Google Cloud Setup

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account
4. Download credentials JSON
5. Share your Google Sheet with the service account email

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/postad/StatsBot.git
cd StatsBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```
BOT_TOKEN=your_bot_token
GOOGLE_SHEETS_URL=your_sheet_url
```

4. Add `credentials.json` file with Google Service Account credentials

5. Run the bot:
```bash
python main.py
```

### Deployment on Railway

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically from main branch

## Project Structure

```
├── main.py                 # Bot entry point
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version
├── Procfile              # Railway deployment config
├── app/
│   ├── sheets_client.py   # Google Sheets integration
│   ├── config/
│   │   └── settings.py    # Configuration
│   └── bot/
│       └── handlers/
│           ├── start.py   # Registration handler
│           └── stats.py   # Statistics handler
└── README.md
```

## How It Works

1. Users start the bot with `/start`
2. Bot asks for dashboard code
3. Code is validated against Google Sheets
4. User is registered and can use `/stats`
5. Statistics are fetched and formatted from Google Sheets

## Security

- Credentials stored as environment variables
- User validation prevents unauthorized access
- One user per company code restriction

## Technologies

- Python 3.11
- aiogram 3.1.1
- Google Sheets API
- Railway (deployment)
- Google Cloud Service Account

## Support

For issues or questions, contact the development team.