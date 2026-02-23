# web/model/board_web.py
class BoardWeb:
    def __init__(self, matrix):
        self.matrix = matrix

    def to_dict(self):
        return {"matrix": self.matrix}
