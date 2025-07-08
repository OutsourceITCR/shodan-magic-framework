from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def create_combined_app():
    """Create a combined Flask app with route prefixes for all services."""
    # Main app to combine all services
    app = Flask(__name__)
    # Create individual apps
    service_auth_app = create_service_auth()
    service_process_manager_app = create_service_process_manager()
    service_client_manager_app = create_service_client_manager()
    service_job_manager_app = create_service_job_manager()

    # Use DispatcherMiddleware to mount services on different prefixes
    app_init.wsgi_app = DispatcherMiddleware(
        app_init.wsgi_app,
        {},
    )

    return app


app = create_combined_app()


if __name__ == '__main__':
    app.run()
