import os

from flask import Flask
from domain.book_domain import db
from resources.book_resource import book_bp

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

app.register_blueprint(book_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
