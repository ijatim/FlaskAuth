from flask import Blueprint, jsonify, request
from src.auth.dal.model.user import User
from utils.jwt_auth import generate_jwt_token
import hashlib
import base64

auth_signin_bp = Blueprint('auth_signin_bp', __name__)


@auth_signin_bp.route('/signin', methods=['POST'])
# Validate inputs
def signin():
    email = request.json['email']
    password = request.json['password']

    # check if email and password are valid
    encrypted_password = base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest())
    user = User.query.filter_by(email=email, password=encrypted_password).first()

    if user is None:
        raise Exception('Provided credentials does not match')

    # let user use app by giving him proper jwt token
    token = generate_jwt_token(user_id=user.id)

    return jsonify(
        {
            'code': 1,
            'message': 'Successful',
            'token': token
        }
    )
