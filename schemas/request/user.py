from marshmallow import Schema, fields, validate

from utils.custom_validations import validate_password


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.And(validate_password))


class RequestRegisterUserSchema(BaseUserSchema):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=30))
    phone_number = fields.Str(required=True, validate=validate.Length(min=10, max=14))


class RequestLoginUserSchema(BaseUserSchema):
    pass
