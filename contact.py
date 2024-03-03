from flask import Flask, request, render_template, redirect, url_for
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)

# Google Sheets API ayarları
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '1xggLZ9HVwbqdixq_vQHMflZQDkBEXgZXeVtYWnyhCUU'  # Google Sheets ID'sini buraya ekleyin
SHEET_NAME = 'Form'  # Verilerin yazılacağı sayfanın adını buraya ekleyin


def append_to_sheet(data):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])
    next_row_index = len(values) + 1
    range_to_update = f"{SHEET_NAME}!A{next_row_index}"
    
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_update,
        valueInputOption='RAW',
        body={'values': [data]}
    ).execute()


@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.form.to_dict()
    # Formdaki alanlara göre verileri Google Sheets'e yaz
    form_values = [
        data.get('input_5'),  # Name
        data.get('input_17'),  # Email Address
        data.get('input_7'),  # Company Name or URL
        data.get('input_18'),  # Budget Range
        data.get('input_8')  # Tell us about your project
    ]
    append_to_sheet(form_values)
    return redirect(url_for('contact'))

@app.route('/contact')
def contact():
    # Contact sayfasını yeniden yükle
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
