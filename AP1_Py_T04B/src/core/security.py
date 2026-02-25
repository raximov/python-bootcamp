import bcrypt
import base64
from functools import wraps
from flask import request, jsonify
from models.user import User


def decode_basic_auth_header(auth_header: str) -> tuple[str, str]:
    """Extract login and password from Authorization header."""
    if not auth_header or not auth_header.startswith("Basic "):
        raise ValueError("Invalid auth header format")

    token = auth_header.split(" ", 1)[1].strip()
    decoded_data = base64.b64decode(token).decode("utf-8")
    login, password = decoded_data.split(":", 1)
    return login, password

def hash_password(password: str) -> str:
    """Parolni bcrypt yordamida heshlash"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(hashed_password: str, plain_password: str) -> bool:
    """Kiritilgan parolni heshlangan parol bilan solishtirish"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class UserAuthenticator:
    @staticmethod
    def validate_credentials(login: str, password: str):
        user = User.query.filter_by(login=login).first()
        if user and check_password(user.password, password):
            return user
        return None

    @staticmethod
    def authenticate(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            try:
                username, password = decode_basic_auth_header(auth_header)
                user = UserAuthenticator.validate_credentials(username, password)
                if not user:
                    raise ValueError("Invalid credentials")
            except Exception:
                return jsonify({'message': 'Login yoki parol xato!'}), 401

            return f(current_user=user, *args, **kwargs)
        return decorated


# Backward-compatible alias used by route decorators.
auth_required = UserAuthenticator.authenticate
