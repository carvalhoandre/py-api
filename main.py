import os
from flask import Flask
from flask_jwt_extended import JWTManager

import secrets

from domain.book_domain import db
from resources.book_resource import book_bp
from resources.user_resource import user_bp
from resources.auth_resource import auth_bp

app = Flask(__name__)

jwt_secret_key = secrets.token_hex(32)

app.config['JWT_SECRET_KEY'] = jwt_secret_key + os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


if not app.config['JWT_SECRET_KEY']:
    raise ValueError("JWT_SECRET_KEY is not set in the environment variables")

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
        print("Database and tables created successfully!")
except Exception as e:
    print(f"Error initializing database: {e}")

app.register_blueprint(book_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
