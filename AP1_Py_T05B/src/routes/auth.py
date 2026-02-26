from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas.auth_req import SignUpRequest
from schemas.jwt import JwtRequest, RefreshJwtRequest, JwtResponse
from services.auth_service import AuthService
from core.security import auth_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    # 1. Parsing and Validation
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "JSON data kutilmoqda (Content-Type: application/json bo'lishi shart)"}), 400
        validated_data = SignUpRequest().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # 2. Business Logic Execution
    response, status_code = AuthService.register(validated_data)
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "JSON data kutilmoqda (Content-Type: application/json bo'lishi shart)"}), 400
        validated_data = JwtRequest().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    response, status_code = AuthService.login(validated_data)
    if status_code == 200:
        # Serialize with JwtResponse schema to ensure correct format (data_key mapping)
        return jsonify(JwtResponse().dump(response)), 200
    return jsonify(response), status_code

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "JSON data kutilmoqda (Content-Type: application/json bo'lishi shart)"}), 400
        validated_data = RefreshJwtRequest().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    response, status_code = AuthService.refresh_access_token(validated_data['refresh_token'])
    if status_code == 200:
        return jsonify(JwtResponse().dump(response)), 200
    return jsonify(response), status_code

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_refresh_token():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "JSON data kutilmoqda (Content-Type: application/json bo'lishi shart)"}), 400
        validated_data = RefreshJwtRequest().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    response, status_code = AuthService.refresh_refresh_token(validated_data['refresh_token'])
    if status_code == 200:
        return jsonify(JwtResponse().dump(response)), 200
    return jsonify(response), status_code

@auth_bp.route('/userinfo', methods=['GET'])
@auth_required
def get_user_info(current_user):
    return jsonify({
        "id": str(current_user.id),
        "login": current_user.login
    }), 200
