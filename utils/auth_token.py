from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_token(user_id, hours=1):
    token = create_access_token(identity=str(user_id), expires_delta=timedelta(hours))
    return token