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
