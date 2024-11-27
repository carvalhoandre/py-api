from repositories.book_repository import BookRepository
from config import db

class BookService:
    def __init__(self):
        self.repository = BookRepository(db.session)

    def get_all_books(self):
        return self.repository.find_all()

    def get_book_by_id(self, book_id):
        return self.repository.find_by_id(book_id)

    def create_book(self, title, author):
        return self.repository.save(title, author)

    def update_book(self, book_id, title, author):
        return self.repository.update(book_id, title, author)

    def delete_book(self, book_id):
        return self.repository.delete(book_id)