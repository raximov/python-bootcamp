from core.database import db
from models.user import User
from core.security import hash_password, UserAuthenticator
from core.jwt_provider import JwtProvider

class UserService:
    @staticmethod
    def get_by_login(login: str) -> User:
        return User.query.filter_by(login=login).first()

    @staticmethod
    def get_by_id(user_id) -> User:
        if isinstance(user_id, str):
            import uuid
            try:
                user_id = uuid.UUID(user_id)
            except ValueError:
                return None
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def create_user(login: str, password: str) -> User:
        hashed_password = hash_password(password)
        new_user = User(login=login, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

class AuthService:
    @staticmethod
    def register(data: dict):
        login = data.get('login')
        password = data.get('password')

        existing_user = UserService.get_by_login(login)
        if existing_user:
            return {"error": "Bunday login band!"}, 409

        new_user = UserService.create_user(login, password)
        return {"success": True, "message": "Foydalanuvchi yaratildi", "id": str(new_user.id)}, 201

    @staticmethod
    def login(data: dict):
        login = data.get('login')
        password = data.get('password')

        user = UserAuthenticator.validate_credentials(login, password)
        if not user:
            return {"error": "Login yoki parol xato!"}, 401

        access_token = JwtProvider.generate_access_token(user)
        refresh_token = JwtProvider.generate_refresh_token(user)

        return {
            "token_type": "Bearer",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

    @staticmethod
    def refresh_access_token(refresh_token: str):
        decoded = JwtProvider.validate_refresh_token(refresh_token)
        if not decoded:
            return {"error": "Refresh token yaroqsiz"}, 401
        
        user_uuid = decoded.get("sub")
        user = UserService.get_by_id(user_uuid)
        if not user:
            return {"error": "Foydalanuvchi topilmadi"}, 401

        new_access_token = JwtProvider.generate_access_token(user)
        return {
            "token_type": "Bearer",
            "access_token": new_access_token,
            "refresh_token": refresh_token
        }, 200

    @staticmethod
    def refresh_refresh_token(refresh_token: str):
        decoded = JwtProvider.validate_refresh_token(refresh_token)
        if not decoded:
            return {"error": "Refresh token yaroqsiz"}, 401
        
        user_uuid = decoded.get("sub")
        user = UserService.get_by_id(user_uuid)
        if not user:
            return {"error": "Foydalanuvchi topilmadi"}, 401

        new_access_token = JwtProvider.generate_access_token(user)
        new_refresh_token = JwtProvider.generate_refresh_token(user)

        return {
            "token_type": "Bearer",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }, 200
