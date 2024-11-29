# config/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import Flask

db = SQLAlchemy()
jwt = JWTManager()

def create_app(env='dev'):
    """Factory function to create the Flask app instance."""
    from config.settings import DevConfig, TestConfig, ProdConfig

    from domain.book_domain import Book
    from domain.user_domain import User

    app = Flask(__name__)

    if env == 'prod':
        app.config.from_object(ProdConfig)
    elif env == 'test':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            if env == 'dev':
                print("Database and tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

    jwt.init_app(app)

    from resources.book_resource import book_bp
    from resources.user_resource import user_bp
    from resources.auth_resource import auth_bp
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    return app
