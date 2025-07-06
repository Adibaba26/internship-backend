from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import requests

app = Flask(__name__)

RECAPTCHA_SECRET_KEY = "6Ld3QXorAAAAAFO4-OdtMwMXbhjMP1GNQp1uPKCU"

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    recaptcha_response = request.form['g-recaptcha-response']

    # Verify reCAPTCHA
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    response = requests.post(verify_url, data=payload)
    result = response.json()

    if not result.get("success"):
        return "reCAPTCHA verification failed. Please try again."

    # Save credentials
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5050, debug=True)
