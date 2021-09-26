from flask import Blueprint, jsonify, request


auth_signup_bp = Blueprint('auth_signup_bp', __name__)

@auth_signup_bp.route('/signup', methods=['POST'])
# validate inputs
def signup():
    # get email
    # get name
    # get password

    # check email existence
    # raise error if email already exists

    # persist hashed password and other related information in database

    # send confirmation email to user

    # we are done here :)

    pass
