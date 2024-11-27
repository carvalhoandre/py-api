from flask import Blueprint, jsonify, request
from service.book_service import BookService

book_bp = Blueprint('books', __name__)
book_service = BookService()

# Retrieve All Books
@book_bp.route('/books', methods=['GET'])
def get_books():
    books = book_service.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200

# Retrieve Book by ID
@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = book_service.get_book_by_id(book_id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({'error': 'Book not found'}), 404

# Create New Book
@book_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('author'):
        return jsonify({"error": "Invalid data"}), 406

    book = book_service.create_book(data['title'], data['author'])
    return jsonify(book.to_dict()), 201

# Update Book
@book_bp.route('/books/<int:id>', methods=['PUT'])
def update_book_by_id(id):
    data = request.get_json()

    if not data or not data.get('title') or not data.get('author'):
        return jsonify({"error": "Invalid data"}), 400

    updated_book = book_service.update_book(id, data['title'], data['author'])

    if not updated_book:
        return jsonify({"error": "Book not found"}), 304

    return jsonify(updated_book.to_dict()), 200

# Delete Book
@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    deleted_book = book_service.delete_book(book_id)

    if not deleted_book:
        return jsonify({"error": "Book not found"}), 304
    return jsonify({'message': 'Book deleted successfully'}), 200


