from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (required for V0 or Vercel frontend)

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Initialize SQLite DB
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Home route (optional - can be removed if not using HTML directly)
@app.route('/')
def index():
    return render_template('login.html')  # You can remove this if only using API

# API route for login form
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract fields safely
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Basic validation
    if not email or not password or not role:
        return jsonify({'success': False, 'error': 'Missing fields'}), 400

    # Store in SQLite
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, password, role))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': {'email': email, 'role': role}
    })

# Optional dashboard route if you're serving templates
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Optional

# Run server
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5080))  # Use 5000 locally, 5080 on PythonAnywhere
    app.run(host='0.0.0.0', port=port, debug=True)
