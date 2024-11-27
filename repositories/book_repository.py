from domain.book_domain import Book

class BookRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def find_all(self):
        return self.db_session.query(Book).all()

    def find_by_id(self, book_id):
        return self.db_session.query(Book).filter_by(id=book_id).first()

    def save(self, title, author):
        new_book = Book(title=title, author=author)
        self.db_session.add(new_book)
        self.db_session.commit()
        return new_book

    def update(self, book_id, title, author):
        book = self.find_by_id(book_id)
        if not book:
            return None
        book.title = title
        book.author = author
        self.db_session.commit()
        return book

    def delete(self, book_id):
        book = self.find_by_id(book_id)
        if not book:
            return None
        self.db_session.delete(book)
        self.db_session.commit()
        return book
