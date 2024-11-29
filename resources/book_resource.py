from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from service.book_service import BookService
from utils.response_http_util import standard_response

book_bp = Blueprint('books', __name__)
book_service = BookService()

# Retrieve All Books
@book_bp.route('/books', methods=['GET'])
def get_books():
    books = book_service.get_all_books()
    data = [book.to_dict() for book in books]
    return standard_response(True, "Books retrieved successfully", 200, data)

# Retrieve Book by ID
@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = book_service.get_book_by_id(book_id)
    if not book:
        return standard_response(False, "Book not found", 400)
    return standard_response(True, "Book retrieved successfully", 200, book.to_dict())

# Create New Book
@book_bp.route('/books', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('author'):
        return standard_response(False, "Invalid data", 400)

    new_book  = book_service.create_book(data['title'], data['author'])
    return standard_response(True, "Book created successfully", 201, new_book.to_dict())

# Update Book
@book_bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book_by_id(book_id):
    data = request.get_json()

    if not data or not data.get('title') or not data.get('author'):
        return standard_response(False, "Invalid data", 400)

    updated_book = book_service.update_book(book_id, data['title'], data['author'])

    if not updated_book:
        return standard_response(False, "Book not found", 400)

    return standard_response(True, "Book updated successfully", 200, updated_book.to_dict())

# Delete Book
@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    deleted_book = book_service.delete_book(book_id)

    if not deleted_book:
        return standard_response(False, "Book not found", 400)
    return standard_response(True, "Book deleted successfully", 200)



