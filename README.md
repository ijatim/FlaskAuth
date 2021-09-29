# FlaskAuth

FlaskAuth is a simple microservice that uses flask as it's core to handle:
* input validation using [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/#) 
* sending emails
* generate jwt tokens

in order to achieve simple sign in and signup scenario.

## Prerequisites

Python3 is a must, and it's suggested to use Python3.6+ for running this microservice.

Install dependencies using **requirements.txt** provided in root directory of project.
```
pip install -r requirements.txt
```

## Configuration
In the **.env** file in root directory of project you'll see all configurations that can be changed by user.
```
SECRET_KEY = 
BACKEND_BASE_URL = https://127.0.0.1:5000
SMTP_SALT = 
DEFAULT_SMTP_EMAIL = 
DEFAULT_SMTP_EMAIL_PASSWORD =
MAIL_SERVER = smtp.gmail.com
MAIL_SERVER_PORT = 587
GOOGLE_CLIENT_ID = 
GOOGLE_CLIENT_SECRET = 
```
Set proper and long **SECRET_KEY** for generating secure jwt token.

**BACKEND_BASE_URL** is domain name of backend service.

Setting **SMTP_SALT** will ensure more secure email generated tokens

Set configured email address for **DEFAULT_SMTP_EMAIL** to send emails using SMTP protocol. By *configured email* it
means **allow less secure app access** for provided email, if not this microservice will not work properly.

Provide **GOOGLE_CLIENT_ID** and **GOOGLE_CLIENT_SECRET** by registering this app to provided email address in your google cloud panel.

## Running
Since this project aims at design level, using this project for ___production___ environments is discouraged. For production purposes **gunicorn**, **docker** and high-end fast **database** are the minimum requirements.

In order to run project simply setup *.env* file and run following command inside root of project.

    //Linux
    [project_root_directory] :$ python3 app.py
    //Windows
    [project_root_directory] > python app.py

### Using google login

By entering following url into your browser you can start process of logging using google account and finnaly you will be redirected to a view which requires token to access.

> https://127.0.0.1:5000/auth/google/signin

Since registered app for default email address in .env file is for **testing** purposes, if you want to login with new gmail you have to register it in google cloud panel. (PASSWORD is available in .env file)

## Swagger

You can access swagger-ui provided to project services by accessing following url:
> https://127.0.0.1:5000/docs

![swagger-ui](docs/swagger/static/auth_swagger.jpg)
