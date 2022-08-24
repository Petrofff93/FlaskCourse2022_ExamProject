from marshmallow import Schema, fields, validate

from utils.custom_validations import (
    validate_password,
    validate_email_already_exists,
    validate_phone_number,
    validate_phone_number_already_exists,
)


class BaseUserSchema(Schema):
    # Custom password and mail validations used in order to prevent violation.
    email = fields.Email(
        required=True, validate=validate.And(validate_email_already_exists)
    )
    password = fields.Str(required=True, validate=validate.And(validate_password))


class RequestRegisterUserSchema(BaseUserSchema):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=30))
    # Custom phone validations used.
    phone_number = fields.Str(
        required=True,
        validate=validate.And(
            validate_phone_number, validate_phone_number_already_exists
        ),
    )


class RequestLoginUserSchema(BaseUserSchema):
    # email fields is overridden in order to prevent the 'mail already exists' exception
    email = fields.Email(required=True)
