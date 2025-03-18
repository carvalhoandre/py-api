import bcrypt
from flask_jwt_extended import get_jwt_identity

from repositories.user_repository import UserRepository
from services.email_service import send_confirmation_email, send_password_email
from utils.auth_token import generate_confirmation_code, generate_token

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_user_by_id(self, user_id):
        try:
            return self.repository.find_by_id(user_id)
        except Exception as e:
            raise ValueError(f"Error finding user by ID: {str(e)}")

    def get_user_by_email(self, email):
        try:
            user = self.repository.find_by_email(email)

            if not user:
                return None

            return user
        except Exception as e:
            raise ValueError(f"Error finding user by email: {str(e)}")

    def update_user(self, user_id, name, email, cpf):
        try:
            return self.repository.update(user_id, name, email, cpf)
        except Exception as e:
            raise ValueError(f"Error updating user: {str(e)}")

    def update_user_password(self, user_id, password, code):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            return self.repository.update_password(user_id, hashed_password, code)
        except Exception as e:
            raise ValueError(f"Error updating user password: {str(e)}")

    def delete_user(self, user_id):
        try:
            return self.repository.delete(user_id)
        except Exception as e:
            raise ValueError(f"Error deleting user: {str(e)}")

    @staticmethod
    def verify_password(hashed_password, plain_password):
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            raise ValueError(f"Error verify password user: {str(e)}")

    def confirm_account(self, user_id, confirmation_code):
        try:
            user = self.repository.active_user(user_id, confirmation_code)
            if not user:
                raise ValueError("Unverified user")

            access_token = generate_token(str(user._id))
            refresh_token = generate_token(str(user._id), 2)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict()
            }
        except Exception as e:
            raise ValueError(f"Error confirming user account: {str(e)}")

    def send_password_reset_email(self, user_email):
        try:
            reset_code = generate_confirmation_code()
            user = self.repository.update_user_code(user_email, reset_code)

            if not user:
                raise ValueError("Failed to find user.")

            send_password_email(
                to_email=user.email,
                subject="Redefina sua senha",
                name=user.first_name,
                user_id=str(user._id),
                reset_code=reset_code
            )

        except Exception as e:
            raise ValueError(f"Error sending password reset email: {str(e)}")

    @staticmethod
    def send_confirmation_email(user):
        try:
            send_confirmation_email(
                to_email=user.email,
                subject="Confirme sua conta",
                confirmation_code=user.confirmation_code,
                name=user.first_name
            )
        except Exception as e:
            raise ValueError(f"Error sending confirmation email: {str(e)}")

    def create_user(self, first_name, last_name, email, cpf, password, role):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            confirmation_code = generate_confirmation_code()

            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hashed_password,
                "cpf": cpf,
                "active": False,
                "confirmation_code": confirmation_code,
                "role": role
            }

            user_id = self.repository.save(user_data)
            saved_user = self.repository.find_by_id(user_id)

            if not saved_user:
                raise ValueError("Failed to create user.")

            return saved_user
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def resending_confirmation_email(self, user_id):
        try:
            confirmation_code = generate_confirmation_code()
            user = self.repository.find_by_id(user_id)

            if not user:
                raise ValueError("User not found.")

            if user.active:
                raise ValueError("User is already verified")

            self.repository.update_confirmation_code(user._id, confirmation_code)
            self.send_confirmation_email(user)

            return user

        except Exception as e:
            raise ValueError(f"Error resending confirmation email: {str(e)}")

    def authentication(self, user, password):
        try:
            if not user:
                raise ValueError("Invalid credentials")

            if not self.verify_password(hashed_password=user.password, plain_password=password):
                raise ValueError("Invalid credentials")

            access_token = generate_token(str(user._id))
            refresh_token = generate_token(str(user._id), 2)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        except Exception as e:
            raise ValueError(f"Error during login: {str(e)}")

    @staticmethod
    def refresh_token():
        try:
            current_user = get_jwt_identity()
            if not current_user:
                raise ValueError("Invalid token or user not found")

            new_access_token = generate_token(current_user)

            return {"access_token": new_access_token}
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error refreshing token: {str(e)}")
