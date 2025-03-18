import os
from pymongo import MongoClient

def get_mongo_db():
    """Returns a MongoDB database connection."""
    environment = os.getenv('FLASK_ENV', 'dev')
    MONGO_URI = os.getenv("DATABASE_MONGO_URI_PROD") if environment == 'prod' else os.getenv("DATABASE_MONGO_URI_DEV")

    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        tls=True,
        tlsAllowInvalidCertificates=False
    )

    try:
        client.admin.command('ping')  # Testa a conexão com o MongoDB
    except Exception as e:
        raise RuntimeError(f"Failed to connect to MongoDB: {e}")

    return client["psi_hub_db"]
