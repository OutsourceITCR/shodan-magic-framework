import logging
import os
from sqlalchemy.exc import IntegrityError

from common.database import init_standalone_db
from common.encryption import encryption_manager
from lib.magic_framework.api.auth.models import User

def get_session_local():
    try:
        return init_standalone_db("common_auth")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        return None

ALLOWED_ENVIRONMENTS = ["development"]

def seed():
    session_local = get_session_local()
    if session_local is None:
        print("Database session could not be initialized.")
        return
    session = session_local()
    admin_password = os.getenv("ADMIN_PASSWORD")
    username = "admin"
    email = "testing2@pridis.com"
    password = admin_password
    hash = encryption_manager.generate_password_hash(password).decode("utf-8")

    try:
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            existing_user.password = hash
            existing_user.email = email
            print(f"Updated user {username} with new password and email.")
        else:
            new_user = User(username=username, email=email, password=hash)
            session.add(new_user)
            print("Seeding Auth User Local")
        session.commit()
    except IntegrityError as error:
        session.rollback()
        if 'UNIQUE constraint failed' in str(error.orig):
            print(f"User with email {email} already exists.")
        else:
            print(f"Error seeding Auth User Local: {error}")