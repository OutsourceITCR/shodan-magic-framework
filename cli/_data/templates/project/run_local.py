import os

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_cors import CORS


def create_combined_app():
    """Create a combined Flask app with route prefixes for all services."""
    # Main app to combine all services
    app_init = Flask(__name__)

    # Create individual apps

    app_init.wsgi_app = DispatcherMiddleware(
        app_init.wsgi_app,
        {},
    )

    return app_init


def init_imported_app(app_imported):
    allowed_origins = [os.getenv("BACKEND_URL")]
    CORS(app_imported, allowed_origins=allowed_origins)

    return app_imported


if __name__ == "__main__":
    app = create_combined_app()
    app.run(host="0.0.0.0", port=4000, debug=True)
