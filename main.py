import os

from flask import Flask, jsonify, request
from models.Book import db, Book

app = Flask(__name__)

env = os.getenv('FLASK_ENV', 'dev')
if env == 'prod':
    app.config.from_object('config.prod.ProdConfig')
elif env == 'test':
    app.config.from_object('config.test.TestConfig')
else:
    app.config.from_object('config.dev.DevConfig')

try:
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("Database connected successfully!")
except Exception as e:
    print("Error initializing database:", e)

# Retrieve All Books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  # Fixed typo
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author } for book in books])

# Retrieve Book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.query.get(id)
    if book:
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author })
    return jsonify({'error': 'Book not found'}), 404

# Create New Book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    book = Book(title=new_book['title'], author=new_book['author'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author })

# Update Book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book_by_id(id):
    updated_book = request.get_json()
    book = Book.query.get(id)
    if book:
        book.title = updated_book['title']
        book.author = updated_book['author']
        db.session.commit()
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author})
    return jsonify({'error': 'Book not found'}), 404

# Delete Book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'error': 'Book not found'}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
