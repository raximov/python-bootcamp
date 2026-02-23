# web/module/__init__.py
from flask import Blueprint

game_blueprint = Blueprint('game', __name__)

# Импортируйте маршруты, чтобы они были зарегистрированы в этом blueprint
from web.route import game_route
