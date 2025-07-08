from common.database import db
from functools import wraps
from flask import request, jsonify


def configure_app(app):
    app.url_map.strict_slashes = False
    app.teardown_appcontext(db_cleanup_session)
    return app


def db_cleanup_session(exception=None):
    if exception:
        db.session.rollback()
    else:
        db.session.commit()
    db.session.remove()


def validate_input(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            if not json_data:
                return jsonify({"message": "No input data provided"}), 400
            errors = schema.validate(json_data)
            if errors:
                return jsonify(errors), 400

            request.validated_data = schema.load(json_data)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
