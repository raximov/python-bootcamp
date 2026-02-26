import uuid
from uuid import UUID
from core.database import db
from models.game import Game, GameStatus
from models.user import User
from core.errors import GameException
from core.security import hash_password
from utils.game_logic import check_winner

class GameService:
    PLAYER_X_SYMBOL = "X"
    PLAYER_O_SYMBOL = "O"
    COMPUTER_LOGIN = "computer_bot"

    @staticmethod
    def create_game(current_user_id: UUID, opponent: str = "user") -> Game:
        if opponent not in ("user", "computer"):
            raise GameException("Opponent faqat 'user' yoki 'computer' bo'lishi mumkin", 400)

        computer_user = None
        if opponent == "computer":
            computer_user = GameService._get_or_create_computer_user()

        new_game = Game(
            player_x_id=current_user_id,
            player_o_id=computer_user.id if computer_user else None,
            status=(
                GameStatus.WAITING_FOR_PLAYERS
                if opponent == "user"
                else GameStatus.PLAYER_TURN
            ),
            current_turn_id=current_user_id
        )
        db.session.add(new_game)
        db.session.commit()
        return new_game

    @staticmethod
    def get_waiting_games():
        return Game.query.filter_by(status=GameStatus.WAITING_FOR_PLAYERS).all()

    @staticmethod
    def get_game_by_id(game_id: UUID) -> Game:
        game = Game.query.filter_by(id=game_id).first()
        if not game:
            raise GameException("O'yin topilmadi", 404)
        return game

    @staticmethod
    def join_game(game_id: UUID, current_user_id: UUID) -> Game:
        game = GameService.get_game_by_id(game_id)
        
        if game.status != GameStatus.WAITING_FOR_PLAYERS:
            raise GameException("O'yin band", 400)
            
        if game.player_x_id == current_user_id:
            raise GameException("O'z o'yiningizga qo'shila olmaysiz", 400)

        # 2chi o'yinchi - O belgisi egasi  
        game.player_o_id = current_user_id
        game.status = GameStatus.PLAYER_TURN
        game.current_turn_id = game.player_x_id
        db.session.commit()
        
        return game

    @staticmethod
    def make_move(game_id: UUID, current_user_id: UUID, position: int) -> Game:
        game = GameService.get_game_by_id(game_id)
        
        if game.status != GameStatus.PLAYER_TURN:
            raise GameException("O'yin tugagan yoki boshlanmagan", 400)

        is_player_x = game.player_x_id == current_user_id
        is_player_o = game.player_o_id == current_user_id
        if not is_player_x and not is_player_o:
            raise GameException("Siz bu o'yin ishtirokchisi emassiz", 403)
            
        if game.current_turn_id != current_user_id:
            raise GameException("Navbat sizniki emas!", 400)

        # Belgini aniqlash: X yoki O
        symbol = GameService.PLAYER_X_SYMBOL if is_player_x else GameService.PLAYER_O_SYMBOL
        idx = position - 1
        board_list = list(game.board)
        
        if board_list[idx] != '-':
            raise GameException("Katak band!", 400)
            
        board_list[idx] = symbol
        game.board = "".join(board_list)
        
        # G'olibni tekshirish
        winner = check_winner(game.board)
        
        if winner:
            GameService._set_game_finished(game, winner)
        else:
            # Agar computer bilan o'ynayotgan bo'lsa, server computer yurishini qiladi
            if GameService._is_vs_computer(game) and symbol == GameService.PLAYER_X_SYMBOL:
                GameService._make_computer_move(game)
            else:
                # Navbatni boshqasiga o'tkazish
                game.current_turn_id = game.player_o_id if symbol == GameService.PLAYER_X_SYMBOL else game.player_x_id
            
        db.session.commit()
        return game

    @staticmethod
    def _is_vs_computer(game: Game) -> bool:
        return bool(game.player_o and game.player_o.login == GameService.COMPUTER_LOGIN)

    @staticmethod
    def _set_game_finished(game: Game, winner: str) -> None:
        if winner == "DRAW":
            game.status = GameStatus.DRAW
            game.winner_id = None
        else:
            game.status = GameStatus.PLAYER_WIN
            game.winner_id = (
                game.player_x_id
                if winner == GameService.PLAYER_X_SYMBOL
                else game.player_o_id
            )
        game.current_turn_id = None

    @staticmethod
    def _make_computer_move(game: Game) -> None:
        idx = GameService._pick_best_move(game.board)
        if idx is None:
            GameService._set_game_finished(game, "DRAW")
            return

        board_list = list(game.board)
        board_list[idx] = GameService.PLAYER_O_SYMBOL
        game.board = "".join(board_list)

        winner = check_winner(game.board)
        if winner:
            GameService._set_game_finished(game, winner)
        else:
            game.current_turn_id = game.player_x_id

    @staticmethod
    def _pick_best_move(board: str):
        board_list = list(board)
        best_score = -float("inf")
        best_move = None

        for idx, cell in enumerate(board_list):
            if cell == "-":
                board_list[idx] = GameService.PLAYER_O_SYMBOL
                score = GameService._minimax(board_list, is_maximizing=False)
                board_list[idx] = "-"
                if score > best_score:
                    best_score = score
                    best_move = idx
        return best_move

    @staticmethod
    def _minimax(board_list, is_maximizing: bool) -> int:
        current_state = check_winner("".join(board_list))
        if current_state == GameService.PLAYER_O_SYMBOL:
            return 10
        if current_state == GameService.PLAYER_X_SYMBOL:
            return -10
        if current_state == "DRAW":
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for idx, cell in enumerate(board_list):
                if cell == "-":
                    board_list[idx] = GameService.PLAYER_O_SYMBOL
                    score = GameService._minimax(board_list, False)
                    board_list[idx] = "-"
                    best_score = max(best_score, score)
            return best_score

        best_score = float("inf")
        for idx, cell in enumerate(board_list):
            if cell == "-":
                board_list[idx] = GameService.PLAYER_X_SYMBOL
                score = GameService._minimax(board_list, True)
                board_list[idx] = "-"
                best_score = min(best_score, score)
        return best_score

    @staticmethod
    def _get_or_create_computer_user() -> User:
        bot = User.query.filter_by(login=GameService.COMPUTER_LOGIN).first()
        if bot:
            return bot

        bot = User(
            login=GameService.COMPUTER_LOGIN,
            password=hash_password(str(uuid.uuid4())),
        )
        db.session.add(bot)
        db.session.flush()
        return bot

    @staticmethod
    def get_completed_games_by_user_uuid(user_uuid: UUID):
        """Retrieve all completed games by user UUID."""
        return Game.query.filter(
            ((Game.player_x_id == user_uuid) | (Game.player_o_id == user_uuid)) &
            ((Game.status == GameStatus.PLAYER_WIN) | (Game.status == GameStatus.DRAW))
        ).order_by(Game.created_at.desc()).all()

    @staticmethod
    def get_top_players(n: int):
        """Retrieve top N players by win ratio."""
        # This is a bit complex for raw SQLAlchemy in a single call without subqueries.
        # Let's use a simpler approach: get all users who played at least one game,
        # then calculate their ratio. Or better, use a SQL query.
        
        # Win ratio = won / (won + lost + drawn)
        # We need to count:
        # games_won: winner_id == user.id
        # games_lost: (player_x_id == user.id or player_o_id == user.id) and status == PLAYER_WIN and winner_id != user.id
        # games_drawn: (player_x_id == user.id or player_o_id == user.id) and status == DRAW
        
        from sqlalchemy import func, case, cast, Float

        # Query to calculate stats per user
        # We'll join User with Game twice (once as player X, once as player O)
        # Or just use union of games where user is X and games where user is O.
        
        # Let's try a direct approach for better performance
        # We'll calculate for each user:
        # wins: games where winner_id == user_id
        # total_completed: games where user is player_x or player_o and status in (PLAYER_WIN, DRAW)
        
        # Since this is a Bootcamp project, I'll stick to a readable but effective query.
        
        subquery = db.session.query(
            User.id.label('user_id'),
            User.login.label('login'),
            func.count(Game.id).label('total_games'),
            func.sum(case((Game.winner_id == User.id, 1), else_=0)).label('wins')
        ).join(
            Game, (Game.player_x_id == User.id) | (Game.player_o_id == User.id)
        ).filter(
            Game.status.in_([GameStatus.PLAYER_WIN, GameStatus.DRAW])
        ).group_by(User.id).subquery()

        results = db.session.query(
            subquery.c.user_id,
            subquery.c.login,
            (cast(subquery.c.wins, Float) / cast(subquery.c.total_games, Float)).label('win_ratio')
        ).order_by((cast(subquery.c.wins, Float) / cast(subquery.c.total_games, Float)).desc()).limit(n).all()

        return [{"id": str(r.user_id), "login": r.login, "win_ratio": round(r.win_ratio, 2)} for r in results]
