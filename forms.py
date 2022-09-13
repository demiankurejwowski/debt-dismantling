from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Name of debt: ')
    submit = SubmitField('Track debt')

class DelForm(FlaskForm):
    id = IntegerField('ID number of debt to remove: ')
    submit = SubmitField("Remove Debt")

class UpdateForm(FlaskForm):
    id = IntegerField('ID of debt to update: ')
    submit = SubmitField("Update Debt")
    