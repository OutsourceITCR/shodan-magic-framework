import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from common.database import db as _db
from lib.magic_frame_py.api.auth.routes import register_routes
from lib.magic_frame_py.api.auth.models import User
from lib.magic_frame_py.api.auth.factories import user_factory
from common.encryption import encryption_manager

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    _db.init_app(app)
    JWTManager(app)
    register_routes(app)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'

@pytest.mark.parametrize(
    "username,password,expected_status,expected_success",
    [
        ("testuser", "testpass", 200, True),  # valid login
        ("nouser", "badpass", 401, False),    # invalid user
        ("testuser", "wrongpass", 401, False), # wrong password
    ]
)
def test_login_parametrized(client, app, username, password, expected_status, expected_success):
    # Use factory to create user for valid login
    if username == "testuser":
        with app.app_context():
            hash = encryption_manager.generate_password_hash("testpass").decode("utf-8")
            user = user_factory(username="testuser", email="test@example.com", password_hash=hash)
            _db.session.add(user)
            _db.session.commit()
    login_data = {"username": username, "password": password}
    resp = client.post('/login', json=login_data)
    assert resp.status_code == expected_status
    assert resp.json['success'] is expected_success
    if expected_success:
        assert 'access_token' in resp.json['data']

def test_register_duplicate_username(client):
    reg_data = {"username": "dupuser", "email": "dup@example.com", "password": "testpass"}
    client.post('/register', json=reg_data)
    resp = client.post('/register', json=reg_data)
    assert resp.status_code == 400
    assert resp.json['success'] is False

def test_me_and_validate(client):
    reg_data = {"username": "meuser", "email": "me@example.com", "password": "testpass"}
    reg_resp = client.post('/register', json=reg_data)
    token = reg_resp.json['data']['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get('/me', headers=headers)
    assert me_resp.status_code == 200
    val_resp = client.get('/validate', headers=headers)
    assert val_resp.status_code == 200
    assert val_resp.json['success'] is True
