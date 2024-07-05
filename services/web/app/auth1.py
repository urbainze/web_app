import db1
from flask_login import current_user
from flask import redirect, url_for, session
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps

SECRET_KEY = "sk_98zdfsas8d49898tyjioer84jmouiyvrdfsfsdqdaz122"
def validate_token(target_role: str = 'user') -> int:
    """
    Validates the session token to check if it matches the required user role.

    #### Parameters:
        `target_role (str)`: The role against which the token's user role is validated. Defaults to 'user'.

    #### Returns:
        `int`: HTTP status code representing the validation result. Possible values:
        - 200 if the token is valid and matches the target_role,
        - 401 if the token is missing, invalid, or expired,
        - 403 if the token's role does not match the target_role.

    Exceptions are handled internally, catching `jwt.ExpiredSignatureError`, and `jwt.InvalidTokenError` to return appropriate HTTP status codes.
    """
    token = session['token']

    if not token:
        return 401 # Unauthorized

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if payload.get('role') in ['admin', target_role]: # Accepts only those with the admin role or target_role 
            return 200
        return 403 # Forbidden
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return 401 # Unauthorized

def create_token(user_id: str, role: str) -> None:
    """
    Creates a JWT token for a given user ID and role and stores it in the session.

    #### Parameters:
        `user_id (str)`: Unique identifier for the user.
        `role (str)`: The role of the user (e.g., 'user', 'admin').

    This function does not return any value but updates the session with the created token.
    The token includes an expiration time set to 8 hours from creation time.
    """
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(hours=8)  # last 8 hours
    }

    # Create token with JWT lib
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    if isinstance(token, bytes):
                
                session['token'] = token.decode('ISO-8859-1')
    else:
                session['token'] = token

def check_credentials(user_id: str, password: str) -> bool:
    """
    Validates user credentials against the database and creates a session token if valid.

    #### Parameters:
        `user_id (str)`: The user's unique identifier.
        `password (str)`: The user's password.

    #### Returns:
        `bool`: True if the credentials are valid and the token was created, False otherwise.
    """
    user_db = db1.UserDatabase()
    user = user_db.get_user_for_login(user_id, password)
    if user:
        create_token(user.user_id, user.role)
        return True
    return False


def token_required(redirect_url: str, target_role: str = 'user'):
    """
    Decorator for routes that require token authentication.

    #### Parameters:
        `redirect_url (str)`: URL to redirect to if token validation fails.
        `target_role (str)`: Role required for the route. Defaults to 'user'.

    #### Returns:
        function: A decorator that can be applied to any route function to enforce token validation.

    The decorator checks for a valid token and the required role, redirecting to the given URL if validation fails.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get('token') and validate_token(target_role) == 200:
                return func(*args, **kwargs)
            return redirect(url_for(redirect_url))
        return wrapper
    return decorator

