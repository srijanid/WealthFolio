from flask import request, jsonify
from functools import wraps
from models import OAuth2Client  # Import your OAuth2Client model from your application

def verify_client_credentials(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_id = request.headers.get('X-Client-ID')  # Use custom headers for security
        client_secret = request.headers.get('X-Client-Secret')

        if not client_id or not client_secret:
            return jsonify({"message": "Client ID and Client Secret are required"}), 401

        client = OAuth2Client.query.filter_by(client_id=client_id, client_secret=client_secret).first()
        if not client:
            return jsonify({"message": "Invalid client credentials"}), 401

        # Pass the client information to the route function if needed
        return f(*args, **kwargs)
    return decorated_function
