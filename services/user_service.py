import bcrypt
from repositories.user_repository import UserRepository
from config import db
from services.email_service import send_confirmation_email, send_password_email

from utils.auth_token import generate_confirmation_code

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

    def verify_password(self, user_id, password):
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        except Exception as e:
            raise ValueError(f"Error verify  password user: {str(e)}")

    def confirm_account(self, user_id, confirmation_code):
        try:
            user_id = int(user_id)
        except Exception as e:
            raise ValueError(f"Error not find user: {str(e)}")

        try:
            return self.repository.active_user(user_id, confirmation_code)
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
                subject="Activate Your Account",
                confirmation_code=user.confirmation_code,
                name=user.name,
                user_id=user.id
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

            self.send_confirmation_email(user)

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
