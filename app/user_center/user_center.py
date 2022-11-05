from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

user_center_bp = Blueprint('user_center_bp', __name__, template_folder='templates')

@user_center_bp.route('/user_center', methods=['GET', 'POST'])
def user_center():
  if current_user.is_authenticated:
    return render_template("user_center.html")
  return redirect(url_for('login_bp.login'))
  

@user_center_bp.route('/user_center/profile', methods=['GET', 'POST'])
@login_required
def profile():
  return render_template("profile.html")

@user_center_bp.route('/user_center/applications', methods=['GET', 'POST'])
@login_required
def applications():
  return render_template("applications.html")

@user_center_bp.route('/user_center/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
  return render_template("analysis.html")