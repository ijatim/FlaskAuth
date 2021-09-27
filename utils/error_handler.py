from flask import Blueprint, jsonify

error_bp = Blueprint('error_bp', __name__)


@error_bp.app_errorhandler(Exception)
def handle_exception(error):
    """
    This function handles all type of raised Exceptions for consistent response of flask view functions
    :param error: an instance of raised Exception
    :return: Response Object of flask
    """
    return jsonify(
        {
            'code': 0,
            'message': str(error)
        }
    )