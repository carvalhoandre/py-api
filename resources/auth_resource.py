from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.user_service import UserService

from utils.response_http_util import standard_response

auth_bp = Blueprint('auth', __name__)
user_service = UserService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return standard_response(False, "Email and password are required", 400)

    try:
        user = user_service.get_user_by_email(email)
        if not user:
            return standard_response(False, "Invalid credentials", 401)

        tokens = user_service.authentication(user, password)

        return standard_response(True, "Login successful", 200, {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "user": user.to_dict()
        })
    except Exception as e:
        return standard_response(False, str(e), 500)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        tokens = user_service.refresh_token()
        return standard_response(True, "Token refreshed successfully", 200, tokens)

    except ValueError as ve:
        return standard_response(False, str(ve), 401)
    except Exception as e:
        return standard_response(False, f"Internal server error: {str(e)}", 500)

@auth_bp.route('/confirm-email', methods=['POST'])
def confirm_email():
    data = request.get_json()
    confirmation_code = data.get('confirmation_code')
    user_id = data.get('user_id')

    if not confirmation_code or not user_id:
        return standard_response(False, "Invalid body request", 400)

    try:
        response = user_service.confirm_account(user_id, confirmation_code)

        return standard_response(True, "Validated successful", 200, {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "user": response["user"]
        })
    except Exception as e:
        return standard_response(False, str(e), 500)

@auth_bp.route('/resend-confirmation-email', methods=['POST'])
def resend_confirm_email():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return standard_response(False, "Invalid body request", 400)

    try:
        user = user_service.resending_confirmation_email(user_id)

        if not user:
            return standard_response(False, "Error resending code", 500)

        return standard_response(True, "Code resent successfully", 200)
    except Exception as e:
        return standard_response(False, str(e), 500)
