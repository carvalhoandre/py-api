from flask_jwt_extended import create_access_token
from datetime import timedelta
import random
import string

def generate_token(user_id, hours=1):
    try:
        return create_access_token(identity=str(user_id), expires_delta=timedelta(hours=hours))
    except Exception as e:
        raise ValueError(f"Error generating token: {str(e)}")

def generate_confirmation_code(length=4):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
