from config import db

from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)
    confirmation_code = db.Column(db.String(36), unique=True)
    role = db.Column(Enum('admin', 'patient', name='user_roles'), nullable=False, default='patient')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "cpf": self.cpf,
            "confirmation_code": self.active,
            "role": self.role
        }
