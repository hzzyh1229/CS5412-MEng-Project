from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from config import Config
from flask_session import Session
from authentication.authentication import login_bp
import os
from home.home import home_bp
from user_center.user_center import user_center_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(user_center_bp)

# to resolve issue in flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.secret_key = "Mario" # necessary step for session
# app.register_blueprint(login_bp, url_prefix='/login')

# @app.route('/')
# def index():
#     """
#     place holder
#     """
#     # return render_template('login.html')
#     return "main page"

if __name__ == "__main__":
    app.run(debug=True)
