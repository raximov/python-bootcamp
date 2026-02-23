# web/route/game_route.py
from flask import request, jsonify, abort
from web.module import game_blueprint
from di.container import container
from web.mapper.game_mapper import GameMapper

@game_blueprint.route('/game2/<game_uuid>', methods=['POST'])
def update_game_2players(game_uuid):
    data = request.get_json()
    if not data:
        abort(400, description="Ma'lumot yo'q")
    try:
        from web.model.game_web import GameWeb
        game_web = GameWeb.from_dict(data)
    except Exception as e:
        abort(400, description=f"Ma'lumotni qayta ishlashda xato: {str(e)}")
    
    # Преобразуем веб-модель в доменную модель
    domain_game = GameMapper.web_to_domain(game_web)
    game_service = container.game_service

    # Если игра уже завершена, возвращаем сообщение о победителе или ничьей
    if game_service.is_game_over(domain_game):
        winner = game_service.get_winner(domain_game.board.matrix)
        if winner == 1:
            message = "O'yin tugadi. X g'olib bo'ldi!"
        elif winner == 2:
            message = "O'yin tugadi. O g'olib bo'ldi!"
        elif winner == 0:
            message = "O'yin tugadi. Durang!"
        else:
            message = "O'yin tugadi."
        response = game_web.to_dict()
        response["message"] = message
        return jsonify(response), 200

    if not game_service.validate_board(domain_game):
        abort(400, description="Noto'g'ri o'yin maydoni holati")
    
    container.game_repository.save_game(domain_game)
    updated_game_web = GameMapper.domain_to_web(domain_game)
    
    # Если после хода игра завершилась, формируем соответствующее сообщение
    if game_service.is_game_over(domain_game):
        winner = game_service.get_winner(domain_game.board.matrix)
        if winner == 1:
            message = "O'yin tugadi. X g'olib bo'ldi!"
        elif winner == 2:
            message = "O'yin tugadi. O g'olib bo'ldi!"
        elif winner == 0:
            message = "O'yin tugadi. Durang!"
        else:
            message = "O'yin tugadi."
    else:
        message = "Qadam qabul qilindi"
    
    response = updated_game_web.to_dict()
    response["message"] = message
    return jsonify(response), 200
