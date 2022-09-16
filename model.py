# db and login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model,UserMixin):

    __tablename__ = 'users'

    user_id         = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(64), unique=True, nullable=False)
    email           = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash   = db.Column(db.String(255), nullable=False)
    state           = db.Column(db.String(2), nullable=True)

    def __init__(self, username="", email="", password="", state=""):
        self.username       = username
        self.email          = email
        self.password_hash  = generate_password_hash(password)
        self.state          = state
        
    def __repr__(self):
        return f'<User ${self.username}>'

class Loans(db.Model):

    __tablename__ = 'loans'

    debt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column