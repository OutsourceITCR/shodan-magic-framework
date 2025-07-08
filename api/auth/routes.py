from datetime import timedelta
from .schemas import UserProfileSchema
from common.flask_hooks import validate_input
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError

from .models import User
from ..schemas import ApiResponseSchema, UserProfileSchema
from .schemas import UserInputSchema, UserLoginInputSchema, LoginOutputSchema, UserOutputSchema
from common.database import db
from common.encryption import encryption_manager
from common.flask_hooks import validate_input
from common.jwt import token_required
from ..schemas import ApiResponseSchema

bp = Blueprint('auth', __name__)


@bp.route('/', methods=['GET'])
def auth_root():
    return make_response(jsonify({'message': 'test route'}), 200)


@bp.route('/login', methods=['POST'])
@validate_input(UserLoginInputSchema())
def auth_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = db.session.query(User).filter(User.username == username).first()
    if user and encryption_manager.check_password_hash(user.password, password):
        access_token = create_access_token(
            identity=str(user.id),
            fresh=True,
            expires_delta=timedelta(hours=48)
        )
        response = {
            "success": True,
            "data": {'access_token': access_token},
            "message": "Login success"
        }
        schema = ApiResponseSchema(data_schema=LoginOutputSchema)
        return schema.dump(response), 200
    
    else:
        response = {"success": False, 'message': 'Invalid email or password'}
        schema = ApiResponseSchema()
        return schema.dump(response), 401


@bp.route('/register', methods=['POST'])
@validate_input(UserInputSchema())
def auth_register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    hash = encryption_manager.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, email=email, password=hash)

    try:
        db.session.add(new_user)
        db.session.flush()
    except IntegrityError as error:
        db.session.rollback()
        schema = ApiResponseSchema()
        response = {"success": False, 'message': 'Username already exists', "errors": [error]}
        return schema.dump(response), 400

    access_token = create_access_token(
        identity=str(new_user.id),
        fresh=True,
        expires_delta=timedelta(hours=48)
    )

    schema = ApiResponseSchema(data_schema=LoginOutputSchema)
    schema_user = UserOutputSchema()
    response = {
        "success": True,
        "data": {
            "user": schema_user.dump(new_user),
            "access_token": access_token
        },
        "message": "User registered successfully"
    }
    return schema.dump(response), 200


@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


@bp.route('/me', methods=['GET'])
@token_required
def me():
    current_user_id = get_jwt_identity()
    token_info = get_jwt()
    return jsonify(user=current_user_id, info=token_info)

@bp.route('/validate', methods=['GET'])
@token_required
def check_token():
    response = {
        "success": True,
        "message": "Token is valid"
    }
    schema = ApiResponseSchema()
    return schema.dump(response), 200


from sqlalchemy.exc import IntegrityError

@bp.route('/profile', methods=['POST'])
@token_required
@validate_input(UserProfileSchema())
def manage_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    schema = ApiResponseSchema(data_schema=UserOutputSchema)
    user = db.session.query(User).filter(User.id == current_user_id).first()
    if not user:
        response = {"success": False, "message": "User not found"}
        return schema.dump(response), 200

    user.name = data['name']
    user.email = data['email']
    user.details = data['details']

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        response = {"success": False, "message": "Email already exists."}
        return schema.dump(response), 200
    except Exception as e:
        db.session.rollback()
        response = {"success": False, "message": "Error updating user", "error": str(e)}
        return schema.dump(response), 200

    response = {
        "success": True,
        "data": schema.data_schema().dump(user),
        "message": "User updated successfully"
    }
    return schema.dump(response), 200

def register_routes(app):
    app.register_blueprint(bp)
