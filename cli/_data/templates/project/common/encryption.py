from flask_bcrypt import Bcrypt

encryption_manager = Bcrypt()


def init_encryption(app):
    encryption_manager.init_app(app)
