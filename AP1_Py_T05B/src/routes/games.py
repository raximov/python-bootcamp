from flask import Blueprint, request, jsonify
from core.security import auth_required
from models.game import Game, GameStatus
from models.user import User
from services.game_service import GameService
from schemas.game_req import MoveRequest, CreateGameRequest
from marshmallow import ValidationError

games_bp = Blueprint('games', __name__, url_prefix='/games')


def _serialize_game(game):
    is_vs_computer = bool(game.player_o and game.player_o.login == GameService.COMPUTER_LOGIN)
    
    # Calculate head-to-head score
    score_x = 0
    score_o = 0
    if game.player_x_id and game.player_o_id:
        # Get all games between these two players that have ended in a win
        h2h_games = Game.query.filter(
            ((Game.player_x_id == game.player_x_id) & (Game.player_o_id == game.player_o_id)) |
            ((Game.player_x_id == game.player_o_id) & (Game.player_o_id == game.player_x_id))
        ).filter(Game.status == GameStatus.PLAYER_WIN).all()
        
        for g in h2h_games:
            if g.winner_id == game.player_x_id:
                score_x += 1
            elif g.winner_id == game.player_o_id:
                score_o += 1

    return {
        'id': str(game.id),
        'board': game.board,
        'status': game.status.value,
        'player_x': str(game.player_x_id) if game.player_x_id else None,
        'player_o': str(game.player_o_id) if game.player_o_id else None,
        'player_x_login': game.player_x.login if game.player_x else None,
        'player_o_login': game.player_o.login if game.player_o else None,
        'winner': str(game.winner_id) if game.winner_id else None,
        'winner_login': User.query.get(game.winner_id).login if game.winner_id else None,
        'current_turn': str(game.current_turn_id) if game.current_turn_id else None,
        'opponent': 'computer' if is_vs_computer else 'user',
        'player_x_mark': 'X',
        'player_o_mark': 'O',
        'score_x': score_x,
        'score_o': score_o
    }


@games_bp.route('', methods=['POST'])
@games_bp.route('/create', methods=['POST'])
@auth_required
def create_game(current_user):
    try:
        data = request.get_json(silent=True) or {}
        validated_data = CreateGameRequest().load(data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 400

    game = GameService.create_game(current_user.id, validated_data['opponent'])
    return jsonify({
        'message': "Yangi o'yin yaratildi", 
        'game': _serialize_game(game)
    }), 201

@games_bp.route('', methods=['GET'])
@auth_required
def get_games(current_user):
    games = GameService.get_waiting_games()
    output = [{'id': str(g.id), 'player_x': str(g.player_x_id), 'opponent': 'user'} for g in games]
    return jsonify({'games': output}), 200

@games_bp.route('/<uuid:game_id>/join', methods=['POST'])
@auth_required
def join_game(current_user, game_id):
    game = GameService.join_game(game_id, current_user.id)
    return jsonify({
        'message': "Qo'shildingiz!", 
        'status': game.status.value
    }), 200

@games_bp.route('/<uuid:game_id>/move', methods=['POST'])
@auth_required
def make_move(current_user, game_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "JSON data kutilmoqda"}), 400
        validated_data = MoveRequest().load(data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 400

    game = GameService.make_move(game_id, current_user.id, validated_data['position'])
    
    return jsonify(_serialize_game(game)), 200

@games_bp.route('/<uuid:game_id>', methods=['GET'])
@auth_required
def get_game_details(current_user, game_id):
    # Dastlab tekshirib olish shartmas o'rtadagi service yopadi, lekin Exception orqali ushlaymiz Error Handlerda
    game = GameService.get_game_by_id(game_id)
    return jsonify(_serialize_game(game)), 200

@games_bp.route('/history', methods=['GET'])
@auth_required
def get_history(current_user):
    games = GameService.get_completed_games_by_user_uuid(current_user.id)
    output = [_serialize_game(g) for g in games]
    return jsonify({'games': output}), 200

@games_bp.route('/leaderboard', methods=['GET'])
@auth_required
def get_leaderboard(current_user):
    # N is passed as query param, default to 10
    n = request.args.get('n', 10, type=int)
    leaderboard = GameService.get_top_players(n)
    return jsonify({'leaderboard': leaderboard}), 200
