import os


class AuthConfig:
    """
    Config class for auth microservice
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    BACKEND_BASE_URL = os.getenv('BACKEND_BASE_URL')
    SMTP_SALT = os.getenv('SMTP_SALT')
    DEFAULT_SMTP_EMAIL = os.getenv('DEFAULT_SMTP_EMAIL')
    DEFAULT_SMTP_EMAIL_PASSWORD = os.getenv('DEFAULT_SMTP_EMAIL_PASSWORD')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_SERVER_PORT = os.getenv('MAIL_SERVER_PORT')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../authdb.sqlite'
    SWAGGER_URL = '/docs'
    SWAGGER_API_URL = '/openapi/auth_swagger.json'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
