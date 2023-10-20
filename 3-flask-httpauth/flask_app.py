from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

# Flask-HTTPAuth is a simple extension that simplifies the use of HTTP 
# authentication with Flask routes.
# Link: https://flask-httpauth.readthedocs.io/en/latest/

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": "secret",
    "jane": "password"
}

# Create a function to verify the username and password
# The function returns True if the username and password are correct,
# and False otherwise. The decorator is defined by Flask-HTTPAuth
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# If the provided credentials are incorrect, Flask-HTTPAuth will 
# handle unauthorized access automatically. You can customize this 
# behavior by defining an error response handler
@auth.error_handler
def unauthorized():
    return "Unauthorized Access", 401

# Create an endpoint that requires authentication
@app.route('/', methods=['POST'])
# The decorator allow you to check if a user is authenticated before 
# granting access to a particular route. It is defined by Flask-HTTPAuth
@auth.login_required
def protected_endpoint():
    data = request.get_json()
    # Your protected endpoint logic goes here
    return f"Received data: {data}"

if __name__ == '__main__':
    app.run()
