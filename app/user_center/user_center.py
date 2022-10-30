from flask import Blueprint, render_template, redirect, url_for, request

user_center_bp = Blueprint('user_center_bp', __name__, template_folder='templates')

@user_center_bp.route('/user_center', methods=['GET', 'POST'])
def user_center():
  return render_template("user_center.html")

@user_center_bp.route('/user_center/profile', methods=['GET', 'POST'])
def profile():
  return render_template("profile.html")

@user_center_bp.route('/user_center/applications', methods=['GET', 'POST'])
def applications():
  return render_template("applications.html")

@user_center_bp.route('/user_center/analysis', methods=['GET', 'POST'])
def analysis():
  return render_template("analysis.html")