from flask import Blueprint, jsonify, request, current_app, url_for, redirect
from utils.schema_validator import ValidationInputType
from utils.decorators import validate_schema
from utils.jwt_auth import generate_jwt_token
from src.auth.dal.model.user import User
from src import db
from .schema import (signin, google_callback)
import requests
import hashlib
import base64
import json

auth_signin_bp = Blueprint('auth_signin_bp', __name__)


def get_google_provider_cfg():
    return requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()


@auth_signin_bp.route('/signin', methods=['POST'])
@validate_schema(signin, input_type=ValidationInputType.BODY)
def signin():
    email = request.json['email']
    password = request.json['password']

    # check if email and password are valid
    encrypted_password = base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest())
    user = User.query.filter_by(email=email, password=encrypted_password).first()

    if user is None:
        raise Exception('Provided credentials does not match. If you have gmail use Google Login option.')

    # let user use app by giving him proper jwt token
    token = generate_jwt_token(user_id=user.id)

    return jsonify(
        {
            'code': 1,
            'message': 'Successful',
            'token': token
        }
    ), 200


@auth_signin_bp.route('/google/signin', methods=['GET'])
def google_signin():
    google_provider_cfg = get_google_provider_cfg()
    if google_provider_cfg.get("authorization_endpoint") is None:
        raise Exception('There is a problem with google provider cfg.')

    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    redirect_uri = current_app.config['BACKEND_BASE_URL'] + url_for('auth_signin_bp.google_callback')
    request_uri = current_app.oauth_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=['openid', 'email', 'profile']
    )

    return redirect(request_uri)


@auth_signin_bp.route('/google/callback', methods=['GET'])
@validate_schema(google_callback, input_type=ValidationInputType.QUERY_PARAM)
def google_callback():
    code = request.args['code']

    google_provider_cfg = get_google_provider_cfg()
    if google_provider_cfg.get("token_endpoint") is None:
        raise Exception('There is a problem with google provider cfg.')

    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = current_app.oauth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config['GOOGLE_CLIENT_ID'], current_app.config['GOOGLE_CLIENT_SECRET']),
    )

    current_app.oauth_client.parse_request_body_response(json.dumps(token_response.json()))

    google_provider_cfg = get_google_provider_cfg()
    if google_provider_cfg.get("token_endpoint") is None:
        raise Exception('There is a problem with google provider cfg.')

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = current_app.oauth_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        email = userinfo_response.json()["email"]
        username = userinfo_response.json()["given_name"]
    else:
        raise Exception('User email not available or not verified by Google.')

    user = User.query.filter_by(email=email, status=1).first()
    if user is None:
        user = User(username=username, email=email, status=1)
        db.session.add(user)
        db.session.commit()

    token = generate_jwt_token(user_id=user.id)

    url = url_for('home_home_bp.home') + f'?token={token}'
    return redirect(url)
