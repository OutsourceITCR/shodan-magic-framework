from marshmallow import Schema, fields, validate, validates, ValidationError
from .models import User
from common.database import db

class UserLoginInputSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)


class UserInputSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    email = fields.Email(required=False, allow_none=True)
    password = fields.String(required=True, allow_none=False)


class UserOutputSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    email = fields.Email(required=False, allow_none=True)


class LoginOutputSchema(Schema):
    access_token = fields.Str(required=True)
    user = fields.Nested(UserOutputSchema(), required=False, default=None)


class UserProfileSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=128),
        error_messages={
            "required": "Name is required.",
            "invalid": "Invalid name.",
            "null": "Name cannot be null."
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email address.",
            "null": "Email cannot be null."
        }
    )
    details = fields.Dict(
        required=True,
        error_messages={
            "required": "Details are required.",
            "invalid": "Details must be a JSON object.",
            "null": "Details cannot be null."
        }
    )
