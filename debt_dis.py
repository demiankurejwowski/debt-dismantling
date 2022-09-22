#server py file
from os import environ
from flask import Flask, render_template, render_template, url_for, redirect, request, flash, abort

from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt

from model import Users, db, database_connection

from forms import AddForm, DelForm, UpdateForm, LoginForm, RegistrationForm




app = Flask(__name__, template_folder='pages')

app.secret_key = environ["secret_key_ftw"]

# basedir = os.path.abspath(os.path.dirname(__file__))

migrate = Migrate(app,db)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)

    return render_template('login.html',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Users(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    state=form.state.data)

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    database_connection(app)
    app.run(debug=True, port=5000)


