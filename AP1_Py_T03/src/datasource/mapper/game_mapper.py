# datasource/mapper/game_mapper.py
from domain.model.game import Game as DomainGame
from datasource.model.game_ds import GameDS
from datasource.model.board_ds import BoardDS

class GameMapper:
    @staticmethod
    def domain_to_ds(domain_game: DomainGame) -> GameDS:
        board_ds = BoardDS(domain_game.board.matrix)
        return GameDS(uuid=domain_game.uuid, board=board_ds)

    @staticmethod
    def ds_to_domain(game_ds: GameDS) -> DomainGame:
        from domain.model.board import Board
        from domain.model.game import Game
        board = Board(matrix=game_ds.board.matrix)
        return Game(uuid=game_ds.uuid, board=board)
