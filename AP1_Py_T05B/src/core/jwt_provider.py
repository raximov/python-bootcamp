from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from models.user import User
from datetime import timedelta

class JwtProvider:
    @staticmethod
    def generate_access_token(user: User) -> str:
        """Generate an accessToken from a User, saving the UUID in the token."""
        return create_access_token(identity=str(user.id))

    @staticmethod
    def generate_refresh_token(user: User) -> str:
        """Generate a refreshToken from a User, saving the UUID in the token."""
        return create_refresh_token(identity=str(user.id))

    @staticmethod
    def validate_access_token(token: str):
        """Method to validate accessToken."""
        try:
            # decode_token will raise errors if expired or invalid
            return decode_token(token)
        except Exception:
            return None

    @staticmethod
    def validate_refresh_token(token: str):
        """Method to validate refreshToken."""
        try:
            return decode_token(token)
        except Exception:
            return None

    @staticmethod
    def extract_uuid(token: str) -> str:
        """Method to extract UUID from the token."""
        decoded = decode_token(token)
        return decoded.get("sub")
