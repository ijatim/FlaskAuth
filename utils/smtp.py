from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path, listdir
from flask import url_for
from enum import Enum
import smtplib
import re


class EmailType(Enum):
    CONFIRMATION = 1


def init_smtp(app):
    """
    This function will register SMTP object to flask app context for further using in service views
    :param app: initialized flask app
    :return: None
    """

    app.email = SMTP(
        default_smtp_email=app.config['DEFAULT_SMTP_EMAIL'],
        password=app.config['MAIL_DEFAULT_SENDER_PASSWORD'],
        server=app.config['MAIL_SERVER'],
        port=app.config['MAIL_SERVER_PORT'],
        secret_key=app.config['SECRET_KEY'],
        salt=app.config['SMTP_PASSWORD_SALT'],
        backend_base_url=app.config['BACKEND_BASE_URL']
    )


# This protocol sends email to user.
class SMTP:
    def __init__(self, default_smtp_email, password, server, port, secret_key, salt, backend_base_url):
        """
        :param default_smtp_email: backend email address for sending email purposes
        :param password: backend email password
        :param server: server that is going to send emails using SMTP protocol
        :param port: server port that is going to send emails using SMTP protocol
        :param secret_key: a string for data serializing and hashing purposes
        :param salt: a string in order to mitigate hash table attacks
        :param backend_base_url: domain address of app
        """
        self.default_smtp_email = default_smtp_email
        self.password = password
        self.server = server
        self.port = port
        self.backend_base_url = backend_base_url
        self.secret_key = secret_key
        self.salt = salt
        self.html_texts_setting = {}
        self.type_to_file_info = {
            EmailType.CONFIRMATION: {"file_name": "confirmation.html",
                                     "subject": 'Confirm your account'}
        }
        self.retry_count = 2
        self.__initialize_html_texts()
        self.__initialize_server()

    def __initialize_server(self):
        if self.__check_connection():
            pass
        else:
            self.connection = smtplib.SMTP(self.server, self.port)
            self.connection.ehlo()
            self.connection.starttls()
            self.connection.login(self.default_smtp_email, self.password)

    def __check_connection(self):
        try:
            status = self.connection.noop()[0]
        except Exception as e:
            status = -1
        return True if status == 250 else False

    def __initialize_html_texts(self):
        html_files_path = path.join(path.dirname(__file__), '../template/email/')
        for file in listdir(html_files_path):
            self.html_texts = {}
            if file.endswith('.html'):
                with open(html_files_path + file, 'r') as html:
                    self.html_texts[file] = html.read()
                    self.html_texts_setting[file] = self.__define_args(self.html_texts[file])

    @staticmethod
    def __define_args(html_text):
        args = re.findall("{.*?}", html_text)
        return args

    def __generate_html_text(self, mail_type, **kwargs):
        html_file_name = self.type_to_file_info[mail_type]['file_name']
        extra_args = self.__generate_html_text_args(html_file_name, kwargs)
        template = self.html_texts[html_file_name].format(**extra_args, **kwargs)
        return template

    def __generate_html_text_args(self, html_file_name, mail_param):
        output_args = {}
        if '{expanding_url}' in self.html_texts_setting[html_file_name]:
            output_args['expanding_url'] = url_for('auth_signup_bp.confirm_email')
        if '{token}' in self.html_texts_setting[html_file_name]:
            output_args['token'] = self.generate_token(mail_param)
        if '{backend_base_url}' in self.html_texts_setting[html_file_name]:
            output_args['backend_base_url'] = self.backend_base_url
        if html_file_name == self.type_to_file_info[EmailType.CONFIRMATION]['file_name']:
            pass

        return output_args

    def generate_token(self, mail_param):
        serializer = URLSafeTimedSerializer(self.secret_key)
        content = f"{mail_param['email_id']}-{mail_param['user_id']}-{mail_param['email']}"
        return serializer.dumps(content, salt=self.salt)

    def confirm_token(self, token, expiration=172800):
        try:
            serializer = URLSafeTimedSerializer(self.secret_key)
            info = serializer.loads(token,
                                    salt=self.salt,
                                    max_age=expiration)
            info = info.split('-')
            return {'email_id': info[0],
                    'user_id': info[1],
                    'email': info[2]}

        except SignatureExpired:
            raise Exception('Your requested url is expired.')

        except Exception as e:
            raise Exception('Server cannot handle your request right now.')

    def send_mail(self, mail_type, receiver_email, **kwargs):
        """
        Sends email generates Exception if failure happens
        :param mail_type: EmailType object to declare which template should be used for generating MIMEText html message
        :param receiver_email: user's email
        :param kwargs: user_id, email_id are required.
        :return: None
        """
        template = self.__generate_html_text(mail_type, **{'email': receiver_email, **kwargs})
        receiver_email = receiver_email
        message = MIMEMultipart()
        message["From"] = self.default_smtp_email
        message["To"] = receiver_email
        message["Subject"] = self.type_to_file_info[mail_type]['subject']
        message["Bcc"] = receiver_email

        message.attach(MIMEText(template, "html"))

        for i in range(self.retry_count):
            self.__initialize_server()
            try:
                self.connection.sendmail(self.default_smtp_email, receiver_email, message.as_string())
                return
            except Exception:
                continue

        raise Exception('SMTP gateway is not available right now.')
