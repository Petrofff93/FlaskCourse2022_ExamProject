from marshmallow import Schema, fields


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RequestRegisterUserSchema(BaseUserSchema):
    first_name = fields.String(min_length=2, max_length=20, required=True)
    last_name = fields.String(min_length=2, max_length=20, required=True)
    phone_number = fields.String(min_length=10, max_length=14, required=True)


class RequestLoginUserSchema(BaseUserSchema):
    pass
