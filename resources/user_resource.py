from flask import Blueprint, jsonify, request
from service.user_service import UserService
from schemas.user_schema import UserSchema

user_bp = Blueprint("users", __name__)
user_service = UserService()
user_schema = UserSchema()

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    errors = user_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    if not data or not data.get('name') or not data.get('email') or not data.get('cpf') or not data.get('password'):
        return jsonify({"error": "Invalid data"}), 406

    user = user_service.create_user( data['name'], data['email'], data['cpf'], data['password'])
    return jsonify(user.to_dict()), 201

@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user_by_id(user_id):
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('cpf'):
        return jsonify({"error": "Invalid data"}), 400

    updated_user = user_service.update_user(user_id, data['name'], data['email'], data['cpf'])

    if not updated_user:
        return  jsonify({"error": "User not found"}), 304

    return jsonify(updated_user.to_dict()), 200

@user_bp.route('/user/password/<int:id>', methods=['PUT'])
def update_user_password(user_id):
    data = request.get_json()

    if not data or data.get('password'):
        return jsonify(({"error": "Invalid data"})), 400

    updated_user_password = user_service.update_user_password(user_id, data["password"])

    if not updated_user_password:
        return jsonify({"error": "User not found"}), 304

    return jsonify(updated_user_password.to_dict()), 200

@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(user_id):
    deleted_user = user_service.delete_user(user_id)

    if not deleted_user:
        return jsonify({"error": "User not found"}), 304
    return jsonify({'message': 'User deleted successfully'}), 200

