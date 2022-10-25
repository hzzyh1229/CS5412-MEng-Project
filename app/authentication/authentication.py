from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .forms import ForgetPassword, LoginForm, RegistrationForm
from models import User
from werkzeug.urls import url_parse

login_bp = Blueprint('login_bp', __name__, template_folder='templates')
# login_bp = Blueprint('login_bp', __name__,
#     template_folder='templates',
#     static_folder='static', static_url_path='assets')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    return the login page
    """
    # if current_user.is_authenticated:
        # return redirect(url_for('task.tasks'))
        # return "user authenticated"
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data.lower()).first()
        # if user is None or not user.check_password(form.password.data):
        #     nologin = True
        # else:
        #     login_user(user, remember=form.remember_me.data)
        #     next_page = request.args.get('next')
        #     if not next_page or url_parse(next_page).netloc != '':
        #         next_page = url_for('task.tasks')
        #     return redirect(next_page)
        return "login success"
    return render_template('authentication/login.html', title='Sign In', form=form)
    # if form.validate_on_submit():
    #     login_user(user)
    #     flask.flash('Logged in successfully.')
    #     # user = models.User.find_by_email(form.email.data)
    # # return render_template('login.html')
    return "log in"

@login_bp.route('/logout')
# @login_required
def logout():
    """
    return the logout page
    """
    # logout_user()
    # return redirect(somewhere)
    flash('Log out successfully.')
    return redirect(url_for('home.home'))

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('task.tasks'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data.lower())
        user.set_password(form.password.data)
        # db.session.add(user)
        # db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('authtication.login'))
    return render_template('authentication/register.html', title='Register', form=form)
    # return "register"

@login_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPassword()
    if form.validate_on_submit():
        return redirect(url_for('authtication.login'))
    return render_template('authentication/forget_password.html', title='Forget', form=form)
    # return "register"

@login_bp.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html')