from flask import Flask, request, make_response

app = Flask(__name__)

# @app.before_request is a decorator that is used to register a function 
# that will be executed before each request is processed by the application
@app.before_request
def set_authorization_header():
    # Check if the "Authorization" header is present in the request
    authorization_header = request.headers.get('Authorization')
    print(f"Authorization Bearer token from request is: client_request_{authorization_header}")

# Create a GET route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')
    authorization_header = request.headers.get('Authorization')
    if username and password and authorization_header and request.method == 'POST':
        return f"Welcome {username}. Your password is {password}. Using Bearer token: {authorization_header}"
    else:
        return f"Welcome to the index page."

# Create a GET route for the protected resource
@app.route('/protected-resource', methods=['GET'])
def protected_resource():
    # Access the "Authorization" header from the request
    # Common practice is to use headers like "X-Auth-Token," "X-API-Key," or something similar
    authorization_header = request.headers.get('Authorization')
    
    # Logic to protect the resource goes here
    if authorization_header is None:
        response = make_response("This is a protected resource. You need to provide a Bearer token in the Authorization header.")
        return response

    # Return the protected resource
    response = make_response(f"Welcome to the protected resource. Bearer token is: {authorization_header}")
    print(f"Authorization Bearer token in response is: server_response_{authorization_header}")
    return response

# Run the app and test in Postman with requests to localhost:5000/ and localhost:5000/protected-resource with a Bearer token in the Authorization header
if __name__ == '__main__':
    app.run()
