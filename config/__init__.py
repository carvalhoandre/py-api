import os
from flask import Flask, request, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.mongo_db import get_mongo_db
from utils import error_handler

jwt = JWTManager()

def create_app(env=None):
    """Factory function to create the Flask app instance."""
    from config.settings import DevConfig, TestConfig, ProdConfig

    env = env or os.getenv('FLASK_ENV', 'dev')

    config_classes = {
        'dev': DevConfig,
        'test': TestConfig,
        'prod': ProdConfig
    }

    app = Flask(__name__)
    app.config.from_object(config_classes.get(env, DevConfig))

    with app.app_context():
        app.config["mongo_db"] = get_mongo_db()

    configure_cors(app)
    configure_jwt(app)
    configure_database(app)
    register_blueprints(app)

    app.register_error_handler(Exception, error_handler.handle_exception)

    return app


def configure_cors(app):
    """Configures CORS settings."""
    cors_origins = os.getenv('BASE_URL', 'http://localhost:3000')
    CORS(app, resources={r"/*": {"origins": cors_origins}}, supports_credentials=True)

    @app.after_request
    def apply_cors_headers(response):
        """Ensures CORS headers are applied correctly."""
        origin = request.headers.get("Origin", cors_origins)
        response.headers.update({
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
        })
        return response


def configure_jwt(app):
    """Initializes JWT settings."""
    jwt.init_app(app)


def configure_database(app):
    """Initializes the MongoDB connection and sets it globally."""

    @app.before_request
    def setup_services():
        try:
            g.mongo_db = get_mongo_db()
        except Exception as e:
            app.logger.error(f"Service initialization failed: {str(e)}")
            raise

    @app.teardown_appcontext
    def teardown_services(exception=None):
        """Ensures database connection is properly closed after each request."""
        g.pop("mongo_db", None)


def register_blueprints(app):
    """Registers Flask blueprints."""
    from resources.user_resource import user_bp
    from resources.auth_resource import auth_bp
    from resources.appointment_resource import appointment_bp
    from resources.schedule_resource import schedule_bp

    blueprints = [user_bp, auth_bp, appointment_bp, schedule_bp]

    for bp in blueprints:
        app.register_blueprint(bp)
