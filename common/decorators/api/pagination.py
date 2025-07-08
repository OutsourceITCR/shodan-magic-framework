from functools import wraps
from flask import request, jsonify


def pagination(default_page=1, default_per_page=10):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):

            try:
                page = request.args.get("page", default_page, type=int)
            except ValueError:
                page = default_page

            pagination = {
                "page": page,
                "per_page": default_per_page,
            }

            return func(*args, pagination_info=pagination, **kwargs)

        return decorated_function
    return decorator
