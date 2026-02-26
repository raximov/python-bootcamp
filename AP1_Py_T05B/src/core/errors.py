from flask import jsonify

class GameException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"message": self.message}

def register_error_handlers(app):
    @app.errorhandler(GameException)
    def handle_game_exception(error):
        return jsonify(error.to_dict()), error.status_code
