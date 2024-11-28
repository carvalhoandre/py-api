import bcrypt
from repositories.user_repository import UserRepository
from config import db

class UserService:
    def __init__(self):
        self.repository = UserRepository(db.session)

    def get_user_by_id(self, user_id):
        return self.repository.find_by_id(user_id)

    def create_user(self, name, email, cpf, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return self.repository.save(name, email, cpf, hashed_password.decode('utf-8'))

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
