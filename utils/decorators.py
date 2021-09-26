from functools import wraps
from enum import Enum


class ValidationInputType(Enum):
    QUERY_PARAM = 1
    URL_PARAM = 2
    BODY = 3


def schema_validator(schema, input_type: ValidationInputType = None):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # initialize validator

            # validate input using validator and schema

            # raise validation errors if available

            # continue executing main function(f)

            return f(*args, **kwargs)

        return wrapped

    return wrapper
