import uuid
from core.database import db
from sqlalchemy.types import Uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.login}>"
