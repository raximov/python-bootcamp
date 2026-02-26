import os
import sys

# src papkasini kompyuter qaerdan ishga tushirishidan qat'iy nazar Python yo'liga qo'shish!
# Bu Linux (Kali/Ubuntu) da ModuleNotFoundError chiqishini oldini oladi.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template
from core.database import db
from core.config import Config
from core.errors import register_error_handlers
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

def create_app():
    # Flask app initialization
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize JWT
    jwt = JWTManager(app)

    # Register standard core error handlers (GameExceptions)
    register_error_handlers(app)

    # Global Exception Handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"message": "Validatsiya xatosi", "errors": error.messages}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        # Logs the actual exception (important for debug)
        print(f"Server xatosi: {e}")
        return jsonify({"message": "Serverda noma'lum xato yuz berdi."}), 500

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/health')
    def health():
        return jsonify({"message": "Tic-Tac-Toe API ishlashga tayyor! Yo'riqnoma uchun api_endpoints.md ni o'qing."}), 200

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.games import games_bp
    from routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(users_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Clean architecture setup means we might want to drop_all or keep
        # Since it's refactoring, let's keep create_all
        db.create_all()
        print("Backend muvaffaqiyatli ishga tushdi...")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
