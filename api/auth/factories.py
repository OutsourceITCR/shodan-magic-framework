from lib.magic_frame_py.api.auth.models import User

def user_factory(username="testuser", email="test@example.com", password_hash="hashedpass"):
    """
    Returns a User instance for testing. Password should be pre-hashed if used in DB.
    """
    return User(username=username, email=email, password=password_hash)

# Example usage in tests:
# user = user_factory(username="foo", email="foo@bar.com", password_hash=hash)
