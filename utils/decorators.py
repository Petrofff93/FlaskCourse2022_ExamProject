from functools import wraps

from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import authentication


def validate_schema(schema_name):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def permission_required(role):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = authentication.current_user()
            if not current_user.role == role:
                raise Forbidden("Permission denied!")
            return func(*args, **kwargs)
        return wrapper
    return decorated_function
