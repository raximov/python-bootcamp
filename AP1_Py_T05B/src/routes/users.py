from flask import Blueprint, jsonify
from core.security import auth_required
from services.auth_service import UserService

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/<uuid:user_id>', methods=['GET'])
@auth_required
def get_user_info(current_user, user_id):
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({'message': 'User topilmadi'}), 404
    return jsonify({'id': str(user.id), 'login': user.login}), 200
