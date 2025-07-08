from flask import Flask
from flask_jwt_extended import JWTManager

from .routes import register_routes
from common.database import init_db
from common.config import get_config
from common.flask_hooks import configure_app
from common.encryption import init_encryption
from common.jwt import init_jwt


def create_app():
    app = Flask(__name__)
    config = get_config()
    app.config.update(config)

    # Initialize database
    init_db(app, schema="common_auth")
    init_encryption(app)
    app = configure_app(app)
    app = init_jwt(app)
    # Register routes
    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=4000)
