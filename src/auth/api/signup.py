from utils.schema_validator import ValidationInputType
from utils.decorators import validate_schema
from flask import Blueprint, jsonify, request, current_app
from .schema import (signup, confirm_email)
from src.auth.dal.model.user import User
from utils.smtp import EmailType
from src import db
import hashlib
import base64

auth_signup_bp = Blueprint('auth_signup_bp', __name__)


@auth_signup_bp.route('/signup', methods=['POST'])
@validate_schema(signup, input_type=ValidationInputType.BODY)
def signup():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    # check input validation
    user = User.query.filter_by(email=email, status=1).first()
    if user is not None:
        raise Exception('There is already an account with this email.')

    # persist hashed password and other related information in database
    encrypted_password = base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest())
    user = User(username=username, email=email, password=encrypted_password, status=2)
    db.session.add(user)
    db.session.commit()

    # send confirmation email to user
    current_app.email.send_mail(mail_type=EmailType.CONFIRMATION,
                                receiver_email=email,
                                email_id=1,
                                user_id=user.id)

    return jsonify(
        {
            'code': 1,
            'message': 'Successful'
        }
    ), 200


@auth_signup_bp.route('/email/confirm', methods=['GET'])
@validate_schema(confirm_email, input_type=ValidationInputType.QUERY_PARAM)
def confirm_email():
    token = request.args['token']
    result = current_app.email.confirm_token(token)
    user_id = result['user_id']
    email = result['email']

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise Exception('Invalid confirmation url.')

    user.status = 1
    db.session.commit()

    pending_users = User.query.filter_by(email=email, status=2).all()
    for user in pending_users:
        user.status = 0
    db.session.commit()

    return jsonify(
        {
            'code': 1,
            'message': 'Successful'
        }
    ), 200
