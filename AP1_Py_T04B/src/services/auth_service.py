from core.database import db
from models.user import User
from core.security import hash_password, decode_basic_auth_header, UserAuthenticator

class UserService:
    @staticmethod
    def get_by_login(login: str) -> User:
        return User.query.filter_by(login=login).first()

    @staticmethod
    def get_by_id(user_id) -> User:
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
    def login(auth_header: str):
        try:
            login, password = decode_basic_auth_header(auth_header)
        except Exception:
            return {"error": "Authorization header noto'g'ri formatda"}, 401

        user = UserAuthenticator.validate_credentials(login, password)
        if user:
            return {"success": True, "id": str(user.id)}, 200
        return {"error": "Login yoki parol xato!"}, 401
