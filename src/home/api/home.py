from flask import Blueprint, render_template
from utils.decorators import token_required
from utils.jwt_auth import TokenLocation

home_home_bp = Blueprint('home_home_bp', __name__)


@home_home_bp.route('', methods=['GET'])
# Passing token is totally discouraged the only purpose of this is for simplicity of redirect without using a webapp
@token_required(location=TokenLocation.ARGS)
def home():
    return render_template('home.html')
