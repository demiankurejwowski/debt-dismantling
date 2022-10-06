#server py file

# from crypt import methods
from email import message
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

        else:
            flash('Incorrect log-in')

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

@app.route('/overview', methods=['GET','POST'])
@login_required
def overview():
    update_form = UpdateForm()
    del_form    = DelForm()
    budget      = MonthlyBudget.query.filter_by(user_id=current_user.id).first()
    loans       = Loans.query.filter_by(user_id=current_user.id).all()
    other       = OtherDebts.query.filter_by(user_id=current_user.id).all()
    cc          = CreditCards.query.filter_by(user_id=current_user.id).all()

    # user.loans - it already does the join statement cause of relationship
    # combined = user.loans + user.other + user.cc
    # sorted = sorted(combined, lambda x: x.current_owed)
    # print(sorted)

    #! Used for loops due to time contraints. Will modify later
    total       = 0
    total_min   = 0
    for x in loans:
        total += x.current_owed
        total_min += x.min_payment
    for y in other:
        total += y.current_owed
        total_min += y.min_payment
    for z in cc:
        total += z.current_owed
        total_min += (z.current_owed * z.min_calc)
    

    # all_d   = Loans.query.join(OtherDebts).join(CreditCards).filter_by(user_id=current_user.id).all()
    # print(all_d)

    return render_template('overview.html', budget=budget, loans=loans, other=other, cc=cc, update_form=update_form, del_form=del_form, total=total, total_min=total_min)

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        if 'loan_delete' in request.form:
            l_id    = request.form['debt_id']
            loan    = Loans.query.filter_by(debt_id=l_id).first()

            db.session.delete(loan)
            db.session.commit()
            flash(f'{loan} was deleted successfully.')

        elif 'other_delete' in request.form:
            o_id    = request.form['other_id']
            debt    = OtherDebts.query.filter_by(other_id=o_id).first()

            db.session.delete(debt)
            db.session.commit()
            flash(f'{debt} was deleted successfully.')

        elif 'cc_delete' in request.form:
            cc_id   = request.form['cc_id']
            cc      = CreditCards.query.filter_by(cc_id=cc_id).first()

            db.session.delete(cc)
            db.session.commit()
            flash(f'{cc} was deleted successfully.')

        else:
            print('error encountered')
  
        
    return redirect(url_for('overview'))

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        if 'loan_edit' in request.form:
            l_id                = request.form['debt_id']
            loan                = Loans.query.filter_by(debt_id=l_id).first()
            update              = request.form['edit_amount']
            loan.current_owed   = update

            db.session.add(loan)
            db.session.commit()
            flash(f'{loan} was updated successfully to {loan.current_owed}.')

        elif 'other_edit' in request.form:
            o_id                = request.form['debt_id']
            debt                = OtherDebts.query.filter_by(other_id=o_id).first()
            update              = request.form['edit_amount']
            debt.current_owed   = update

            db.session.add(debt)
            db.session.commit()
            flash(f'{debt} was updated successfully to {debt.current_owed}.')

        elif 'cc_edit' in request.form:
            cc_id               = request.form['debt_id']
            cc                  = CreditCards.query.filter_by(cc_id=cc_id).first()
            update              = request.form['edit_amount']
            cc.current_owed     = update
            db.session.add(cc)
            db.session.commit()
            flash(f'{cc} was updated successfully to {cc.current_owed}.')

        else:
            print('error encountered')

    return redirect(url_for('overview'))

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
        flash(f"{loan.loan_name} has been added to your list.")
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
        flash(f'{other.debt_name} has been added to your list.')
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
        flash(f'{cc.card_name} has been added to your list.')
        return redirect(url_for('debtadded'))
        

    return render_template('addnew.html', loan_form=loan_form, other_form=other_form, cc_form=cc_form, budget_form=budget_form)

@app.route('/debtadded')
@login_required
def debtadded():
    return render_template('debtadded.html')

if __name__ == '__main__':
    database_connection(app)
    app.run(debug=True, port=8000)


