import os
import sqlite3
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Get the path to the database file
dir = os.path.dirname(__file__)
db = os.path.join(dir, 'users.db')

admin_bearer_token = "mikkel_1337"

# Create table users if not exists
with sqlite3.connect(db) as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")

# Create a before request function to check if the "Authorization" header is present in the request
@app.before_request
def set_authorization_header():
    # Check if the "Authorization" header is present in the request
    authorization_header = request.headers.get('Authorization')
    if authorization_header is None:
        return jsonify({"status": "error", "message": "You need to provide a Bearer token in the Authorization header."}), 401

# Create a get route for the index page
@app.route('/')
def index():
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
    return jsonify(users, 200)

# Create a post route to authenticate admin user
@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    # Access the "Authorization" header from the request
    authorization_header = request.headers.get('Authorization')
    if authorization_header != admin_bearer_token:
        error_response = make_response(jsonify({"status": "error", "message": "You need to provide a valid Bearer token in the Authorization header."}), 401)
        error_response.set_cookie('admin_bearer_token', authorization_header)
        return error_response
    succes_response = make_response(jsonify({"status": "success", "message": "You are authenticated."}), 200)
    succes_response.set_cookie('admin_bearer_token', admin_bearer_token)
    return succes_response

# Create a post route to receive JSON data and add a new person to the database
@app.route('/api/users', methods=['POST'])
def create_user():
    # Access the "Authorization" header from the request
    authorization_header = request.headers.get('Authorization')
    print(authorization_header)
    if authorization_header != admin_bearer_token:
        return jsonify({"status": "error", "message": "You need to provide a valid Bearer token in the Authorization header."}), 401
    # Access the "Cookie" header from the request
    admin_bearer_token_cookie = request.cookies.get('admin_bearer_token')
    if admin_bearer_token_cookie != admin_bearer_token:
        return jsonify({"status": "error", "message": "You need to provide a valid cookie token in the Cookie header."}), 401
    # If request body is not JSON or request body is wrong, return an error
    try:
        if not request.json:
            return jsonify({"status": "error", "message": "The request body must be JSON"}), 400
    except:
        return jsonify({"status": "error", "message": "The request body must be JSON"}), 400
    email = request.json.get('email')
    password = request.json.get('password')
    data = (email, password)
    # Insert the new user into the database
    try:
        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", data)
        return jsonify({"status": "success", "message": "User created"}, 201)
    except:
        return jsonify({"status": "error", "message": "Something went wrong"}, 400)

# Run the app and test in Postman using a Bearer token in the Authorization header to get a cookie token in the Cookie header
if __name__ == '__main__':
    app.run()
