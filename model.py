# db and login_manager

from os import environ
from xmlrpc.client import DateTime
from werkzeug.security import generate_password_hash, check_password_hash
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

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    


class Loans(db.Model):

    __tablename__ = 'loans'

    debt_id         = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    loan_name       = db.Column(db.String(64), nullable=False, unique=True)
    current_owed    = db.Column(db.Float, nullable=False)
    interest_rate   = db.Column(db.Float, nullable=False)
    min_payment     = db.Column(db.Float, nullable=False)
    due_date        = db.Column(db.DateTime, nullable=False)
    payoff_date     = db.Column(db.DateTime, nullable=False)
    active          = db.Column(db.Boolean, nullable=False)

    def __init__(self, loan_name="", current_owed = "", interest_rate="", min_payment="", due_date="", payoff_date="", active=True):
        self.loan_name      = loan_name
        self.current_owed   = current_owed
        self.interest_rate  = interest_rate
        self.min_payment    = min_payment
        self.due_date       = due_date
        self.payoff_date    = payoff_date
        self.active         = active

    def __repr__(self):
        return f'Something to return'

class OtherDebts(db.Model):

    __tablename__ = 'other_debts'

    other_id        = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    debt_name       = db.Column(db.String(64), nullable=False)
    current_owed    = db.Column(db.Float, nullable=False)
    interest_rate   = db.Column(db.Float, nullable=False)
    min_payment     = db.Column(db.Float, nullable=True)
    due_date        = db.Column(db.DateTime, nullable=False)
    payoff_date     = db.Column(db.DateTime, nullable=False)
    active          = db.Column(db.Boolean, nullable=False)

    def __init__(self, debt_name="", current_owed="", interest_rate="", min_payment="", due_date="", payoff_date="", active=True):
        self.debt_name      = debt_name
        self.current_owed   = current_owed
        self.interest_rate  = interest_rate
        self.min_payment    = min_payment
        self.due_date       = due_date
        self.payoff_date    = payoff_date
        self.active         = active
    
    def __repr__(self):
        return f'Something to return'

class CreditCards(db.Model):

    __tablename__ = 'credit_cards'

    cc_id           = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    card_name       = db.Column(db.String(64), nullable=False)
    card_max        = db.Column(db.Integer, nullable=False)
    current_owed    = db.Column(db.Float, nullable=False)
    interest_rate   = db.Column(db.Float, nullable=False)
    due_date        = db.Column(db.DateTime, nullable=False)
    min_calc        = db.Column(db.Float, nullable=True)
    active          = db.Column(db.Boolean, nullable=False)

    def __init__(self, card_name="", card_max="", current_owed="", interest_rate="", due_date="", min_calc="", active=True):
        self.card_name      = card_name
        self.card_max       = card_max
        self.current_owed   = current_owed
        self.interest_rate  = interest_rate
        self.due_date       = due_date
        self.min_calc       = min_calc
        self.active         = active

    def __repr__(self):
        return f'Something to return'

def database_connection(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['POSTGRES_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from debt_dis import app
    database_connection(app)
    print("Connected")

