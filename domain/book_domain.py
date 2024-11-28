from config import db

class Book(db.Model):
        __tablename__ = 'books'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(150), nullable=False)
        author = db.Column(db.String(100), nullable=False)

        def to_dict(self):
                return {
                        "id": self.id,
                        "title": self.title,
                        "author": self.author
                }