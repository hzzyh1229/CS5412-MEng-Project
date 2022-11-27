from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .forms import ForgetPassword, LoginForm, RegistrationForm
from models import User
from werkzeug.urls import url_parse
from azure.cosmos import CosmosClient
# from .. import app

import requests
API_BASE = "https://cs5412cloudjobboard.azurewebsites.net/"

login_bp = Blueprint('login_bp', __name__, template_folder='templates')
# login_bp = Blueprint('login_bp', __name__,
#     template_folder='templates',
#     static_folder='static', static_url_path='assets')
URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Users'
container = database.get_container_client(CONTAINER_NAME)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    return the login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
        # return "user authenticated"
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user_info = list(container.query_items(
            query='SELECT * FROM Users WHERE Users.email = @email', 
                parameters=[dict(name="@email", value=form.email.data)], 
                enable_cross_partition_query=True))
        # user_info = requests.get(API_BASE + f"users/{form.email.data}").json()
        if user_info and len(user_info) == 1 and User.check_password(user_info[0]['password'], form.password.data):
            user_obj = User(email=user_info[0]['email'], nickname=user_info[0]['name'])
            login_user(user_obj)
            flash('You have successfully logged in')
            return redirect(url_for('home.home'))
        else:
            error = 'Password is incorrect'
    return render_template('authentication/login.html', title='Sign In', form=form, error=error)

@login_bp.route('/logout')
@login_required
def logout():
    """
    return the logout page
    """
    logout_user()
    flash('Log out successfully.')
    return redirect(url_for('home.home'))

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_obj = User(email=form.email.data, password=form.password.data, nickname=form.nickname.data)
        user_obj.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login_bp.login'))
    return render_template('authentication/register.html', title='Register', form=form)

@login_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPassword()
    if form.validate_on_submit():
        return redirect(url_for('authtication.login'))
    return render_template('authentication/forget_password.html', title='Forget', form=form)

@login_bp.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html')