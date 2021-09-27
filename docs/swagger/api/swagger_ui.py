from flask import send_from_directory, Blueprint

docs_swagger_ui_bp = Blueprint('docs_swagger_ui_bp', __name__)


@docs_swagger_ui_bp.route('/openapi/<path:path>')
def send_swagger(path):
    """
    Provides json specification for OpenAPI3
    :param path: the path to swagger json specification
    :return: flask Response object based on .json swagger specification file
    """
    return send_from_directory('../docs/swagger/static', path)
