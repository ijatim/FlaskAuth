from utils.schema_validator import ValidationInputType
from flask import current_app, request
from utils.jwt_auth import verify_jwt_token, TokenLocation
from functools import wraps


def token_required(location: TokenLocation = TokenLocation.HEADER):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            verify_jwt_token(location=location)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def validate_schema(schema, input_type: ValidationInputType = None):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            schema_validator = current_app.schema_validator
            try:
                errors = schema_validator.get_errors(request, kwargs, schema, input_type)
            except Exception as e:
                raise e
            if not errors:
                return f(*args, **kwargs)
            else:
                raise Exception(errors[0].message)

        return wrapped

    return wrapper
