#server py file

# from crypt import methods
from os import environ
from flask import Flask, render_template, render_template, url_for, redirect, request, flash, abort

from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from model import CreditCards, Loans, MonthlyBudget, OtherDebts, Users, db, database_connection
from forms import LoanForm, OtherForm, CCForm, DelForm, UpdateForm, LoginForm, RegistrationForm, BudgetForm



app = Flask(__name__, template_folder='pages')

app.secret_key = environ["SECRET_KEY_FTW"]

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
        user = Users(email      =form.email.data,
                    username    =form.username.data,
                    password    =form.password.data,
                    state       =form.state.data)

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#todo: Currently working on showing the data from the tables
#! Right here look at me lol

@app.route('/overview', methods=['GET','POST'])
@login_required
def overview():
    # update_form = UpdateForm()
    budget  = MonthlyBudget.query.filter_by(user_id=current_user.id).first()
    loans   = Loans.query.filter_by(user_id=current_user.id).all()
    other   = OtherDebts.query.filter_by(user_id=current_user.id).all()
    cc      = CreditCards.query.filter_by(user_id=current_user.id).all()
    print(other)
    print(cc)
    # for loan in all_loans:
    #     print(loan.loan_name)
    return render_template('overview.html', budget=budget, loans=loans, other=other, cc=cc)

@app.route('/addnew', methods=['GET','POST'])
@login_required
def addnew():
    loan_form   = LoanForm()
    other_form  = OtherForm()
    cc_form     = CCForm()
    budget_form = BudgetForm()
    user        = current_user
    get_budget  = MonthlyBudget.query.filter_by(user_id=current_user.id).first()

    if budget_form.validate_on_submit():
        if get_budget:
            get_budget.spending_amount = budget_form.spending_amount.data

            db.session.add(get_budget)
            db.session.commit()
            flash(f'Monthly budget has been set at ${get_budget.spending_amount}')

        else:
            budget = MonthlyBudget( user_id         = user.id,
                                    spending_amount = budget_form.spending_amount.data)

            db.session.add(budget)
            db.session.commit()
            flash(f'Monthly budget has been set at ${budget.spending_amount}')
    
        return redirect(url_for('debtadded'))

    if loan_form.validate_on_submit():
        loan = Loans(user_id        = user.id,
                    loan_name       = loan_form.loan_name.data,
                    current_owed    = loan_form.current_owed_l.data,
                    interest_rate   = loan_form.interest_rate_l.data,
                    min_payment     = loan_form.min_payment_l.data,
                    due_date        = loan_form.due_date_l.data,
                    payoff_date     = loan_form.payoff_date_l.data)

        db.session.add(loan)
        db.session.commit()
        flash("Loan has been added to your list.")
        return redirect(url_for('debtadded'))


    if other_form.validate_on_submit():
        other = OtherDebts( user_id         = user.id,
                            debt_name       = other_form.debt_name.data,
                            current_owed    = other_form.current_owed_o.data,
                            interest_rate   = other_form.interest_rate_o.data,
                            min_payment     = other_form.min_payment_o.data,
                            due_date        = other_form.due_date_o.data,
                            payoff_date     = other_form.payoff_date_o.data)
        
        db.session.add(other)
        db.session.commit()
        flash('Debt has been added to your list.')
        return redirect(url_for('debtadded'))


    if cc_form.validate_on_submit():
        cc = CreditCards(user_id        = user.id,
                        card_name       = cc_form.card_name.data,
                        card_max        = cc_form.card_max_cc.data,
                        current_owed    = cc_form.current_owed_cc.data,
                        interest_rate   = cc_form.interest_rate_cc.data,
                        due_date        = cc_form.due_date_cc.data,
                        min_calc        = cc_form.min_calc_cc.data)

        db.session.add(cc)
        db.session.commit()
        flash('CreditCard has been added to your list.')
        return redirect(url_for('debtadded'))
        

    return render_template('addnew.html', loan_form=loan_form, other_form=other_form, cc_form=cc_form, budget_form=budget_form)

@app.route('/debtadded')
@login_required
def debtadded():
    return render_template('debtadded.html')

if __name__ == '__main__':
    database_connection(app)
    app.run(debug=True, port=8000)


