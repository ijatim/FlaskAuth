from src import db


class User(db.Model):
    """
    Defines a user that interacts with system
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(250))
    password = db.Column(db.String(128))
    status = db.Column(db.Integer)
