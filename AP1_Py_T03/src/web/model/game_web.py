# web/model/game_web.py
class GameWeb:
    def __init__(self, uuid, board):
        self.uuid = uuid
        self.board = board  # ожидается список списков (матрица)

    def to_dict(self):
        return {"uuid": self.uuid, "board": self.board}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(uuid=data.get("uuid"), board=data.get("board"))
