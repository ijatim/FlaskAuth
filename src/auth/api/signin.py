from flask import Blueprint, jsonify, request


auth_signin_bp = Blueprint('auth_signin_bp', __name__)


@auth_signin_bp.route('/signin', methods=['POST'])
def signin():
    # get user's email
    # get user's password

    # check if email and password are valid
    # raise error if password is not correct

    # let user use app by giving him proper jwt token or by any other means.
    pass
