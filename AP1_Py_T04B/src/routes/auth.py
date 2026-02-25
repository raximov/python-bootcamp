from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas.auth_req import SignUpRequest
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    # 1. Parsing and Validation
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON data kutilmoqda"}), 400
        validated_data = SignUpRequest().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # 2. Business Logic Execution
    response, status_code = AuthService.register(validated_data)
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    auth_header = request.headers.get("Authorization")
    response, status_code = AuthService.login(auth_header)
    return jsonify(response), status_code
