from bson import ObjectId
from flask import current_app
from domain.user_domain import User

class UserRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        return current_app.config["mongo_db"]

    def find_all(self):
        users = self.get_db()["users"].find()
        return [User.from_dict(user) for user in users]

    def find_by_id(self, user_id):
        user = self.get_db()["users"].find_one({"_id": ObjectId(user_id)})
        return User.from_dict(user) if user else None

    def save(self, user_data):
        result = self.get_db()["users"].insert_one(user_data)

        if not result.inserted_id:
            raise ValueError("User could not be created.")

        return str(result.inserted_id)

    def update_password(self, user_id, hashed_password, code):
        user = self.find_by_id(user_id)
        if not user or user.confirmation_code != code:
            return None

        self.get_db()["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password, "confirmation_code": None}}
        )
        return self.find_by_id(user_id)

    def update(self, user_id, name, email, cpf):
        self.get_db()["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"first_name": name.split()[0], "last_name": " ".join(name.split()[1:]), "email": email, "cpf": cpf}}
        )
        return self.find_by_id(user_id)

    def active_user(self, user_id, confirmation_code):
        user = self.find_by_id(user_id)
        if not user or user.confirmation_code != confirmation_code:
            return None

        self.get_db()["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"active": True, "confirmation_code": None}}
        )
        return self.find_by_id(user_id)

    def delete(self, user_id):
        user = self.find_by_id(user_id)
        if not user:
            return None

        self.get_db()["users"].delete_one({"_id": ObjectId(user_id)})
        return User.from_dict(user)

    def find_by_email(self, email):
        user_data = self.get_db()["users"].find_one({"email": email})

        return User.from_dict(user_data) if user_data else None

    def update_confirmation_code(self, user_id, confirmation_code):
        self.get_db()["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"confirmation_code": confirmation_code, "active": False}}
        )
        return self.find_by_id(user_id)

    def update_user_code(self, user_email, code):
        user = self.find_by_email(user_email)
        if not user:
            return None

        self.get_db()["users"].update_one(
            {"_id": ObjectId(user._id)},
            {"$set": {"confirmation_code": code}}
        )
        return self.find_by_id(user._id)
