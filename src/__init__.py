from flask import Flask
from dotenv import load_dotenv


def create_flask_app():
    load_dotenv()  # Exporting all variables that are defined in .env file to system environment variables
    app = Flask(__name__)

    # register flask blueprints
    from src.auth.api.signin import auth_signin_bp
    from src.auth.api.signup import auth_signup_bp
    from utils.error_handler import error_bp

    app.register_blueprint(auth_signin_bp, url_prefix='/auth')
    app.register_blueprint(auth_signup_bp, url_prefix='/auth')
    app.register_blueprint(error_bp)

    # load config of auth microservice
    app.config.from_object('config.AuthConfig')

    # initialize specific utils for auth microservice like database, smtp and etc
    from utils.smtp import init_smtp
    init_smtp(app)

    return app
