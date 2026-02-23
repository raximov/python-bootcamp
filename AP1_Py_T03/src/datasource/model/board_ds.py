# datasource/model/board_ds.py
class BoardDS:
    def __init__(self, matrix):
        self.matrix = matrix

    def __repr__(self):
        return f"BoardDS({self.matrix})"
