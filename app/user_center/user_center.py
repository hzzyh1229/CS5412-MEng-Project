from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from azure.cosmos import CosmosClient

user_center_bp = Blueprint('user_center_bp', __name__, template_folder='templates')
URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Users'
container = database.get_container_client(CONTAINER_NAME)

@user_center_bp.route('/user_center', methods=['GET', 'POST'])
def user_center():
  if current_user.is_authenticated:
    # print(current_user.get_username())
    return render_template("user_center.html")
  return redirect(url_for('login_bp.login'))
  

@user_center_bp.route('/user_center/profile', methods=['GET', 'POST'])
@login_required
def profile():
  username = current_user.get_username()['email']
  # print(username)
  nickname = current_user.get_nickname()
  # print(nickname)
  return render_template("profile.html", email=username, nickname=nickname)

@user_center_bp.route('/user_center/applications', methods=['GET', 'POST'])
@login_required
def applications():
  return render_template("applications.html")

@user_center_bp.route('/user_center/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
  return render_template("analysis.html")