# domain/model/game.py
import uuid
from domain.model.board import Board

class Game:
    def __init__(self, uuid=None, board: Board = None):
        self.uuid = uuid or str(uuid.uuid4())
        self.board = board or Board()

    def __repr__(self):
        return f"Game(uuid={self.uuid}, board={self.board})"
