import bcrypt
from functools import wraps
from flask import request, jsonify
from models.user import User
from core.jwt_provider import JwtProvider


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
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({'message': 'Authorization header kutilmoqda (Bearer token)'}), 401

            token = auth_header.split(" ", 1)[1].strip()
            decoded = JwtProvider.validate_access_token(token)
            
            if not decoded:
                return jsonify({'message': 'Yaroqsiz yoki muddati o\'tgan token'}), 401

            user_uuid = decoded.get("sub")
            from services.auth_service import UserService
            user = UserService.get_by_id(user_uuid)
            
            if not user:
                return jsonify({'message': 'Foydalanuvchi topilmadi'}), 401

            return f(current_user=user, *args, **kwargs)
        return decorated


# Backward-compatible alias used by route decorators.
auth_required = UserAuthenticator.authenticate
