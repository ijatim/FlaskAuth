from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask

db = SQLAlchemy()


def create_flask_app():
    """
    Initialize flask app and registers all dependencies like blueprints, urls, handlers and etc
    :return: flask app object
    """
    load_dotenv()  # Exporting all variables that are defined in .env file to system environment variables
    app = Flask(__name__)

    # load config of auth microservice
    app.config.from_object('config.AuthConfig')

    # register flask blueprints
    from src.auth.api.signin import auth_signin_bp
    from src.auth.api.signup import auth_signup_bp
    from utils.error_handler import error_bp
    from docs.swagger.api.url import register_docs_blueprint

    app.register_blueprint(auth_signin_bp, url_prefix='/auth')
    app.register_blueprint(auth_signup_bp, url_prefix='/auth')
    app.register_blueprint(error_bp)
    register_docs_blueprint(app)

    # initialize specific utils for auth microservice like database, smtp and etc
    from utils.smtp import init_smtp
    from utils.schema_validator import init_schema_validator

    init_smtp(app)
    init_schema_validator(app)

    # initialize database
    from src.auth.dal.model.user import User
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app
