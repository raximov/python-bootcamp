# di/container.py
from datasource.repository.game_repository import GameRepository
from domain.service.game_service_impl import GameServiceImpl

class Container:
    def __init__(self):
        self.game_repository = GameRepository()
        self.game_service = GameServiceImpl(self.game_repository)

# Глобальный экземпляр контейнера, который можно импортировать в других модулях.
container = Container()
