import gspread
from oauth2client.service_account import ServiceAccountCredentials


def test_connection():
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)

        sheet_url = 'https://docs.google.com/spreadsheets/d/1k4sQCH30fDpXKeO0mHbtzBHlKWvHAA5udyAzZXDBm5w'
        sheet_id = sheet_url.split('/')[5]
        sheet = client.open_by_key(sheet_id).sheet1

        data = sheet.get_all_records()
        print(f'Data received. Quantity: {len(data)}')

        if data:
            print(f'First row: {data[0]}')

    except Exception as e:
        print(f'Error: {str(e)}')
        print(f'Error type: {type(e).__name__}')


if __name__ == '__main__':
    test_connection()
