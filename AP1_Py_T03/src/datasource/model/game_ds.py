# datasource/model/game_ds.py
from datasource.model.board_ds import BoardDS

class GameDS:
    def __init__(self, uuid, board: BoardDS):
        self.uuid = uuid
        self.board = board

    def __repr__(self):
        return f"GameDS(uuid={self.uuid}, board={self.board})"
