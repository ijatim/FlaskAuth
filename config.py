import os


class AuthConfig:
    """
    Config class for auth microservice
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    BACKEND_BASE_URL = os.getenv('BACKEND_BASE_URL')
    SMTP_PASSWORD_SALT = os.getenv('SMTP_PASSWORD_SALT')
    DEFAULT_SMTP_EMAIL = os.getenv('DEFAULT_SMTP_EMAIL')
    MAIL_DEFAULT_SENDER_PASSWORD = os.getenv('MAIL_DEFAULT_SENDER_PASSWORD')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_SERVER_PORT = os.getenv('MAIL_SERVER_PORT')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SWAGGER_URL = os.getenv('SWAGGER_URL')
    SWAGGER_API_URL = os.getenv('SWAGGER_API_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
