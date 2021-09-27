from flask import send_from_directory, Blueprint

docs_swagger_ui_bp = Blueprint('docs_swagger_ui_bp', __name__)


@docs_swagger_ui_bp.route('/openapi/<path:path>')
def send_swagger(path):
    return send_from_directory('../docs/swagger/static', path)