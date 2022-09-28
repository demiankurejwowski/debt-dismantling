
from inspect import Attribute
from tokenize import String
from turtle import update
from unicodedata import name
from wsgiref.validate import validator
from xmlrpc.client import DateTime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator, Length
from wtforms.fields import DateField
import email_validator

from model import Users

class LoginForm(FlaskForm):
    username    = StringField('Username',validators=[DataRequired()])
    password    = PasswordField('Password',validators=[DataRequired()])
    submit      = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email               = StringField('Email',validators=[DataRequired(),Email()])
    username            = StringField('Username', validators=[DataRequired()])
    password            = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm',message="Passwords don't match")])
    password_confirm    = PasswordField('Confirm Password',validators=[DataRequired()])
    #todo: Needs to be changed to SelectField - list of 50 states and default=none
    state               = StringField('State', validators=[Length(max=2)])
    submit              = SubmitField('Register')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered')

    def check_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has already been registered')

class LoanForm(FlaskForm):
    loan_name       = StringField('Loan Name',validators=[DataRequired()])
    current_owed_l  = StringField('Current Amount Owed', validators=[DataRequired()])
    interest_rate_l = StringField('Interest Rate',validators=[DataRequired()])
    min_payment_l   = StringField('Minimum Payment Amount',validators=[DataRequired()])
    due_date_l      = DateField('Due Date', format='%Y-%m-%d',validators=[DataRequired()])
    payoff_date_l   = DateField('Payoff Date', format='%Y-%m-%d',validators=[DataRequired()])
    submit_l        = SubmitField('Track Loan', name='loan')

class OtherForm(FlaskForm):
    debt_name       = StringField('Debt Name', validators=[DataRequired()])
    current_owed_o  = StringField('Current Amount Owed', validators=[DataRequired()])
    interest_rate_o = StringField('Interest Rate', validators=[DataRequired()])
    min_payment_o   = StringField('Minimum Payment Amount')
    due_date_o      = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    payoff_date_o   = DateField('Payoff Date (if applicable)', format='%Y-%m-%d', validators=[DataRequired()])
    submit_o        = SubmitField('Track Debt', name='other')

class CCForm(FlaskForm):
    card_name       = StringField('CreditCard Name', validators=[DataRequired()])
    card_max_cc     = StringField('Card Max Amount', validators=[DataRequired()])
    current_owed_cc = StringField('Current Amount Owed', validators=[DataRequired()])
    interest_rate_cc= StringField('Interest Rate', validators=[DataRequired()])
    min_calc_cc     = StringField('Minimum Calculation Amount')
    due_date_cc     = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit_cc       = SubmitField('Track CreditCard', name='cc')

class BudgetForm(FlaskForm):
    spending_amount = StringField('Monthly Budget Amount ', validators=[DataRequired()])
    submit_b        = SubmitField('Submit Budget', name='budget')
class DelForm(FlaskForm):
    delete  = StringField('Remove')
    submit  = SubmitField('Detele')

class UpdateForm(FlaskForm):
    update        = StringField('Redacted')
    submit        = SubmitField("Update Debt")

    