from flask_jwt_extended import create_access_token
from datetime import timedelta
import random
import string

def generate_token(user, hours=1):
    token = create_access_token(identity={"id": user.id, "active": user.active}, expires_delta=timedelta(hours))
    return token

def generate_confirmation_code(length=4):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def active_required(func):
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        jwt_data = get_jwt()
        if not jwt_data.get("active"):
            return standard_response(False, "User account is inactive", 403)
        return func(*args, **kwargs)
    return wrapper
    