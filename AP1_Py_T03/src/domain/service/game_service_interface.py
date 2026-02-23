# domain/service/game_service_interface.py
from abc import ABC, abstractmethod
from domain.model.game import Game

class GameServiceInterface(ABC):
    @abstractmethod
    def next_move(self, game: Game) -> Game:
        """Вычисляет следующий ход текущей игры по алгоритму Минимакс."""
        pass

    @abstractmethod
    def validate_board(self, game: Game) -> bool:
        """Проверяет корректность игрового поля (не изменены ли предыдущие ходы)."""
        pass

    @abstractmethod
    def is_game_over(self, game: Game) -> bool:
        """Проверяет, завершена ли игра."""
        pass
