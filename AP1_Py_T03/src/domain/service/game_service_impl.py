# domain/service/game_service_impl.py
from domain.service.game_service_interface import GameServiceInterface
from domain.model.game import Game

class GameServiceImpl(GameServiceInterface):
    def __init__(self, repository):
        self.repository = repository

    def next_move(self, game: Game) -> Game:
        board = game.board.matrix
        if self.is_game_over(game):
            return game

        best_score = -float('inf')
        best_move = None

        # Простой перебор возможных ходов для компьютера (алгоритм Минимакс)
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = self.minimax(board, is_maximizing=False)
                    board[i][j] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            board[best_move[0]][best_move[1]] = 2

        return game

    def validate_board(self, game: Game) -> bool:
        board = game.board.matrix
        count_x = sum(row.count(1) for row in board)
        count_o = sum(row.count(2) for row in board)
        if count_x != count_o and count_x != count_o + 1:
            return False
        if self.check_winner(board, 1) and self.check_winner(board, 2):
            return False
        return True

    def is_game_over(self, game: Game) -> bool:
        board = game.board.matrix
        return self.get_winner(board) is not None

    def check_winner(self, board, player: int) -> bool:
        # Проверка строк
        for row in board:
            if all(cell == player for cell in row):
                return True
        # Проверка столбцов
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        # Проверка диагоналей
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def get_winner(self, board) -> int:
        """
        Возвращает:
          1, если выигрывают крестики (X);
          2, если выигрывают нолики (O);
          0, если ничья;
          None, если игра не завершена.
        """
        if self.check_winner(board, 1):
            return 1
        if self.check_winner(board, 2):
            return 2
        if all(cell != 0 for row in board for cell in row):
            return 0  # ничья
        return None

    def minimax(self, board, is_maximizing: bool) -> int:
        if self.check_winner(board, 2):
            return 10
        if self.check_winner(board, 1):
            return -10
        if all(cell != 0 for row in board for cell in row):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2
                        score = self.minimax(board, False)
                        board[i][j] = 0
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, True)
                        board[i][j] = 0
                        best_score = min(best_score, score)
            return best_score
