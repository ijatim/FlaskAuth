from flask import current_app, request
from enum import Enum
import datetime
import jwt


class TokenLocation(Enum):
    HEADER = 1
    ARGS = 2

def generate_jwt_token(jwt_secret_key: str = '', **kwargs):
    """
    Generates a jwt token for further authentication use cases
    :param jwt_secret_key: secret_key for encrypting jwt token
    :param kwargs: additional data for token payload
    :return: jwt token
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15, seconds=5),
        **kwargs
    }
    jwt_token = jwt.encode(
        payload,
        jwt_secret_key if jwt_secret_key else current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return "Bearer " + jwt_token


def get_jwt_token_payload(token: str = ''):
    """
    Gets payload from token input if not available from flask request object Authorization header
    :param token: jwt token
    :return:
    """
    if not token:
        token = request.headers.get('Authorization')

    if not token:
        raise Exception('Please provide Authorization token.')

    token = token.replace('Bearer ', '')
    return jwt.decode(token, verify=False)


def verify_jwt_token(location: TokenLocation = TokenLocation.HEADER, token: str = ''):
    """
    Verifies signature of provided jwt token
    :param location: location where token header lives
    :param token: jwt token
    :return:
    """
    if not token:
        if location == TokenLocation.HEADER:
            token = request.headers.get('Authorization')
        else:
            token = request.args.get('token')

    if not token:
        raise Exception('Please provide Authorization token.')

    token = token.replace('Bearer ', '')
    try:
        jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
    except Exception as e:
        raise Exception(str(e))
