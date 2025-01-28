import bcrypt
from flask_jwt_extended import get_jwt_identity

from repositories.user_repository import UserRepository
from config import db
from services.email_service import send_confirmation_email, send_password_email

from utils.auth_token import generate_confirmation_code, generate_token

class UserService:
    def __init__(self):
        self.repository = UserRepository(db.session)

    def get_user_by_id(self, user_id):
        try:
            return self.repository.find_by_id(user_id)
        except Exception as e:
            raise ValueError(f"Error find user by id: {str(e)}")

    def get_user_by_email(self, email):
        try:
            return self.repository.find_by_email(email)
        except Exception as e:
            raise ValueError(f"Error find user by email: {str(e)}")

    def update_user(self, user_id, name, email, cpf):
        try:
            return self.repository.update(user_id, name, email, cpf)
        except Exception as e:
            raise ValueError(f"Error update user: {str(e)}")

    def update_user_password(self, user_id, password):
        try:
            return self.repository.update_password(user_id, password)
        except Exception as e:
            raise ValueError(f"Error update password user: {str(e)}")

    def delete_user(self, user_id):
        try:
            return self.repository.delete(user_id)
        except Exception as e:
            raise ValueError(f"Error delete user: {str(e)}")

    @staticmethod
    def verify_password(user_password, password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8'))
        except Exception as e:
            raise ValueError(f"Error verify password user: {str(e)}")

    def confirm_account(self, user_id, confirmation_code):
        try:
            user_id = int(user_id)

        except Exception as e:
            raise ValueError(f"Error not find user: {str(e)}")

        try:
            user = self.repository.active_user(user_id, confirmation_code)

            if not user:
                raise ValueError("Unverified user")

            access_token = generate_token(user.id)
            refresh_token = generate_token(user.id, 2)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict()
            }

        except Exception as e:
            raise ValueError(f"Error confirm account user: {str(e)}")

    def send_password_reset_email(self, user_email):
        try:
            reset_code = generate_confirmation_code()

            user = self.repository.find_by_email(user_email)

            if not user:
                raise ValueError("Failed to find user.")

            send_password_email(
                to_email=user.email,
                subject="Redefina a sua senha",
                name=user.name,
                user_id=user.id,
                reset_code=reset_code
            )

        except Exception as e:
            raise ValueError(f"Error send email: {str(e)}")

    @staticmethod
    def send_confirmation_email(user):
        try:
            send_confirmation_email(
                to_email=user.email,
                subject="Confirme sua conta",
                confirmation_code=user.confirmation_code,
                name=user.name
            )
        except Exception as e:
            raise ValueError(f"Error sending confirmation email: {str(e)}")

    def create_user(self, name, email, cpf, password, role):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            confirmation_code = generate_confirmation_code()

            user = self.repository.save(name, email, cpf, hashed_password, confirmation_code, role)

            if not user:
                raise ValueError("Failed to create user.")

            return user
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def resending_confirmation_email(self, user_id):
        try:
            confirmation_code = generate_confirmation_code()
            user = self.repository.find_by_id(user_id)

            if not user:
                raise ValueError("User not found.")

            if user.active:
                raise ValueError("user is already verified")

            self.repository.update_confirmation_code(user, confirmation_code)

            self.send_confirmation_email(user)

            return user

        except Exception as e:
            raise ValueError(f"Error resending confirmation email: {str(e)}")

    def authentication(self, user_id, password):
        try:
            user = self.get_user_by_id(user_id)

            if not user:
                raise ValueError("Invalid credentials")

            if not self.verify_password(user.password, password):
                raise ValueError("Invalid credentials")

            if not user.active:
                self.send_confirmation_email(user)
                raise ValueError("Account not activated. A new confirmation email has been sent.")

            access_token = generate_token(user.id)
            refresh_token = generate_token(user.id, 2)

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
            new_access_token = generate_token(current_user)

            if not new_access_token:
                raise ValueError("Invalid credentials")
            return new_access_token

        except Exception as e:
            raise ValueError(f"Error refresh token: {str(e)}")