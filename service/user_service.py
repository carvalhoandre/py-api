import bcrypt
from repositories.user_repository import UserRepository
from config import db
from service.email_service import send_confirmation_email

from utils.auth_token import generate_confirmation_code

class UserService:
    def __init__(self):
        self.repository = UserRepository(db.session)

    def get_user_by_id(self, user_id):
        return self.repository.find_by_id(user_id)

    def get_user_by_email(self, email):
        return self.repository.find_by_email(email)

    def create_user(self, name, email, cpf, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        confirmation_code = generate_confirmation_code()

        user = self.repository.save(name, email, cpf, hashed_password, confirmation_code)

        if not user:
            return None

        try:
            send_confirmation_email(
                to_email=email,
                subject="Activate Your Account",
                confirmation_code=confirmation_code,
                name=name,
                user_id=user.id
            )
            print(f"Confirmation email sent to {email}")
        except Exception as e:
            print(f"Error sending email: {e}")

        return user

    def update_user(self, user_id, name, email, cpf):
        return self.repository.update(user_id, name, email, cpf)

    def update_user_password(self, user_id, password):
        return self.repository.update_password(user_id, password)

    def delete_user(self, user_id):
        return self.repository.delete(user_id)

    def verify_password(self, user_id, password):
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

    def confirm_account(self, user_id, confirmation_code):
        try:
            user_id = int(user_id)
        except ValueError:
            return None

        return self.repository.active_user(user_id, confirmation_code)