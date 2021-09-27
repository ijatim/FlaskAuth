from flask_swagger_ui import get_swaggerui_blueprint
from docs.swagger.api.swagger_ui import docs_swagger_ui_bp


def register_docs_blueprint(app):
    app.register_blueprint(docs_swagger_ui_bp)

    swagger_url = app.config['SWAGGER_URL']
    API_URL = app.config['SWAGGER_API_URL']
    swagger_ui_bp = get_swaggerui_blueprint(
        swagger_url,
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Auth API Helper"
        }
    )

    app.register_blueprint(swagger_ui_bp, url_prefix=swagger_url)
