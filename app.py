
import os
import sqlite3
import subprocess
import hashlib
import requests
from flask import Flask, request

app = Flask(__name__)

# TEST ONLY: Fake secret for Secret Scanning practice.
# This is NOT a real credential.
API_KEY = "ghp_1234567890abcdef1234567890abcdef123456"

# Example 1: SQL Injection vulnerability
@app.route("/user")
def get_user():
    username = request.args.get("username", "")

    connection = sqlite3.connect("users.db")

    query = "SELECT * FROM users WHERE username = '" + username + "'"

    result = connection.execute(query).fetchall()

    connection.close()

    return str(result)


# Example 2: Command Injection vulnerability
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")

    result = subprocess.check_output(
        "ping -c 1 " + host,
        shell=True
    )

    return result.decode()


# Example 3: Insecure hash algorithm
@app.route("/hash")
def create_hash():
    password = request.args.get("password", "")

    hashed = hashlib.md5(password.encode()).hexdigest()

    return hashed


# Example 4: Hardcoded credential usage
@app.route("/external")
def external_api():
    headers = {
        "Authorization": "Bearer " + API_KEY
    }

    response = requests.get(
        "https://example.com/api",
        headers=headers,
        timeout=5
    )

    return str(response.status_code)


@app.route("/")
def home():
    return "GitHub Security Testing Lab"


if __name__ == "__main__":
    app.run(debug=True)
