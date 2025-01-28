from flask import Blueprint, request
from services.user_service import UserService
from schemas.user_schema import UserSchema
from utils.response_http_util import standard_response

user_bp = Blueprint("users", __name__)
user_service = UserService()
user_schema = UserSchema()

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return standard_response(False, "User not found", 404)

    try:
        return standard_response(True, "User retrieved successfully", 200, user.to_dict())
    except Exception as e:
        return standard_response(False, str(e), 500)

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)

    if errors:
        return standard_response(False, "Invalid data", 400)

    try:
        new_user = user_service.create_user(
            data['name'], data['email'], data['cpf'], data['password'], data['role']
        )
        return standard_response(True, "User created successfully", 201, new_user.to_dict())
    except Exception as e:
        return standard_response(False, str(e), 500)


@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('cpf'):
        return standard_response(False, "Invalid data", 400)

    try:
        updated_user = user_service.update_user(user_id, data['name'], data['email'], data['cpf'])

        if not updated_user:
            return standard_response(False, "User not found", 400)

        return standard_response(True, "User updated successfully", 200, updated_user.to_dict())
    except Exception as e:
        return standard_response(False, str(e), 500)

@user_bp.route('/user/reset-password/<int:user_id>', methods=['PUT'])
def update_user_password(user_id):
    data = request.get_json()
    new_password = data["password"]
    token = data["token"]

    if not token or not new_password:
        return standard_response(False, "Invalid data", 400)

    try:
        updated_user_password = user_service.update_user_password(user_id, password = new_password, code=token)

        if not updated_user_password:
            return standard_response(False, "User not found", 400)

        return standard_response(True, "Password updated successfully", 200)
    except Exception as e:
        return standard_response(False, str(e), 500)

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted_user = user_service.delete_user(user_id)

    if not deleted_user:
        return standard_response(False, "User not found", 400)

    try:
        return standard_response(True, "User deleted successfully", 200)
    except Exception as e:
        return standard_response(False, str(e), 500)

@user_bp.route('/user/forgot-password', methods=['POST'])
def send_password_reset_email():
    try:
        data = request.get_json()
        user_email = data.get('email')

        if not data or not user_email:
            return standard_response(False, "Invalid email", 400)

        user_service.send_password_reset_email(user_email)

        return standard_response(True, "Email sent successfully", 200)
    except Exception as e:
        return standard_response(False, str(e), 500)