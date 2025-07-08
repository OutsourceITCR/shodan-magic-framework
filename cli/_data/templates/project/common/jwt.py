import os
from functools import wraps
from flask import jsonify

from flask_jwt_extended import JWTManager, verify_jwt_in_request


def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    return app


# Decorators
def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Automatically checks the token
        except Exception as e:
            return jsonify({"message": "Invalid or missing token", "error": str(e)}), 401
        return fn(*args, **kwargs)

    return wrapper
