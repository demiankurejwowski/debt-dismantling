import os
from forms import AddForm, DelForm, UpdateForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy()

class Users(db.Model):

    __tablename__ = 'users'
    id - db.Column(db.Integer, primary_key=True)
