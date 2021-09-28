signin = {
    'required': ['email', 'password'],
    'properties': {
        'email': {'type': 'string', 'maxLength': 250,
                  'pattern': r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,63})$"},
        'password': {'type': 'string', 'minLength': 6, 'maxLength': 30}
    }
}

signup = {
    'required': ['email', 'username', 'password'],
    'properties': {
        'username': {'type': 'string', 'minLength': 2, 'maxLength': 25},
        'email': {'type': 'string', 'maxLength': 250,
                  'pattern': r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,63})$"},
        'password': {'type': 'string', 'minLength': 6, 'maxLength': 30}
    }
}

confirm_email = {
    'required': ['token'],
    'properties': {
        'token': {'type': 'string'}
    }
}

google_callback = {
    'required': ['code']
}
