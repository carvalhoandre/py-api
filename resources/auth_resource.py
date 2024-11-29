from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from service.user_service import UserService

from utils.response_http_util import standard_response
from utils.auth_token import generate_token

auth_bp = Blueprint('auth', __name__)
user_service = UserService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = user_service.get_user_by_email(email)
    if not user or not user_service.verify_password(user.id, password):
        return standard_response(False, "Invalid credentials", 401)

    access_token = generate_token(user.id)
    refresh_token = generate_token(user.id, 2)

    return standard_response(True, "Login successful", 200, {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    })

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = generate_token(current_user)
    return standard_response(True, "Login successful", 200, {
        "access_token": new_access_token
    })