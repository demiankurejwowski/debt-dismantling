#server py file

import os
from forms import AddForm, DelForm, UpdateForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt



app = Flask(__name__)



