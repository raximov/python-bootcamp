# domain/model/board.py
class Board:
    def __init__(self, matrix=None):
        # Инициализация игрового поля 3x3, если не задано иное
        if matrix is None:
            self.matrix = [[0 for _ in range(3)] for _ in range(3)]
        else:
            self.matrix = matrix

    def __repr__(self):
        return f"Board({self.matrix})"
