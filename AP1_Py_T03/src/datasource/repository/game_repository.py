# datasource/repository/game_repository.py
import threading
from datasource.model.game_ds import GameDS

class GameRepository:
    def __init__(self):
        self._games = {}
        self._lock = threading.Lock()

    def save_game(self, game: GameDS):
        with self._lock:
            self._games[game.uuid] = game

    def get_game(self, uuid) -> GameDS:
        with self._lock:
            return self._games.get(uuid)
