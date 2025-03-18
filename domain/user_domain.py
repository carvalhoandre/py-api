from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(
            self,
            first_name,
            last_name,
            email,
            password,
            cpf,
            active=True,
            confirmation_code=None,
            role="user",
            _id=None
    ):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.cpf = cpf
        self.active = active
        self.confirmation_code = confirmation_code
        self.role = role

        if password.startswith("$2b$"):
            self.password = password
        else:
            self.password = generate_password_hash(password)

    def to_dict(self, include_password=False):
        user_data = {
            "_id": str(self._id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "cpf": self.cpf,
            "active": self.active,
            "confirmation_code": self.confirmation_code,
            "role": self.role
        }
        if include_password:
            user_data["password"] = self.password
        return user_data

    @staticmethod
    def from_dict(data):
        return User(
            _id=data.get("_id"),
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            cpf=data["cpf"],
            active=data.get("active", True),
            confirmation_code=data.get("confirmation_code"),
            role=data.get("role", "user")
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)
