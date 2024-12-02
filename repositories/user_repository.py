from domain.user_domain import User

class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def find_all(self):
        return self.db_session.query(User).all()

    def find_by_id(self, user_id):
        return self.db_session.query(User).filter_by(id=int(user_id)).first()

    def save(self, name, email, cpf, password, confirmation_code, role):
        new_user = User(
            name=name,
            email=email,
            cpf=cpf,
            password=password,
            confirmation_code=confirmation_code,
            role=role,
            active=False
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def update_password(self, user_id, password):
        user = self.find_by_id(user_id)
        if not user:
            return None
        user.password = password
        self.db_session.commit()
        return user

    def update(self, user_id, name, email, cpf):
        user = self.find_by_id(user_id)
        if not user:
            return None
        user.name = name
        user.email = email
        user.cpf = cpf
        self.db_session.commit()
        return user

    def active_user(self, user_id, confirmation_code):
        user = self.find_by_id(user_id)

        if not user or user.confirmation_code != confirmation_code:
            return None

        user.active = True
        user.confirmation_code = None
        self.db_session.commit()
        return user

    def delete(self, user_id):
        user = self.find_by_id(user_id)
        if not user:
            return None
        self.db_session.delete(user)
        self.db_session.commit()
        return user

    def find_by_email(self, email):
        return self.db_session.query(User).filter_by(email=email).first()