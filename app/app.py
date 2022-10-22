from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from config import Config
from authentication.authentication import login_bp
import os
from home.home import home_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp, url_prefix="/")

bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
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
