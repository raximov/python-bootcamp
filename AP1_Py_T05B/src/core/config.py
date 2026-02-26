import os

class Config:
    # Primary setup for T04 is PostgreSQL via SQLAlchemy.
    # Override with DATABASE_URL in environment if needed.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/tictactoe",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Kelajakda JWT yoki session ishlatsak kerak bo'lishi mumkin
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_super_secret_key_123')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key_456_very_long_and_secure_key_32_chars')
    # Optional: set token expiration
    from datetime import timedelta
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
