from functools import wraps
from flask import request, jsonify


def order(default_order, default_direction="ASC"):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                order = request.args.get("order", default_order, type=str)
                order_direction = request.args.get("direction", default_direction, type=str)
            except ValueError:
                order = default_order
                order_direction = default_direction

            order = {
                "order": order,
                "direction": order_direction,
            }

            return func(*args, order_info=order, **kwargs)

        return decorated_function
    return decorator
