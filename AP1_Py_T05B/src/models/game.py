import enum
import uuid
from core.database import db
from sqlalchemy.types import Uuid

class GameStatus(str, enum.Enum):
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    PLAYER_TURN = "PLAYER_TURN"
    DRAW = "DRAW"
    PLAYER_WIN = "PLAYER_WIN"

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board = db.Column(db.String(9), default="-" * 9)
    status = db.Column(db.Enum(GameStatus), default=GameStatus.WAITING_FOR_PLAYERS)
    
    # ForeignKey relationships
    player_x_id = db.Column(Uuid(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    player_o_id = db.Column(Uuid(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    
    # State tracking
    current_turn_id = db.Column(Uuid(as_uuid=True), nullable=True)
    winner_id = db.Column(Uuid(as_uuid=True), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relationships (Optional but useful for querying)
    player_x = db.relationship("User", foreign_keys=[player_x_id])
    player_o = db.relationship("User", foreign_keys=[player_o_id])

    def __repr__(self):
        return f"<Game {self.id} - {self.status.value}>"
