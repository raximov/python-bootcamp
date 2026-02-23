# web/mapper/game_mapper.py
from web.model.game_web import GameWeb
from domain.model.game import Game

class GameMapper:
    @staticmethod
    def domain_to_web(domain_game: Game) -> GameWeb:
        return GameWeb(uuid=domain_game.uuid, board=domain_game.board.matrix)

    @staticmethod
    def web_to_domain(game_web: GameWeb) -> Game:
        from domain.model.board import Board
        board = Board(matrix=game_web.board)
        return Game(uuid=game_web.uuid, board=board)
