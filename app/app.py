from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from config import Config
from flask_session import Session
from authentication.authentication import login_bp
import os
from home.home import home_bp
from user_center.user_center import user_center_bp
from authentication.authentication import login_bp
from flask_login import LoginManager
from models import User
from azure.cosmos import CosmosClient

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp, url_prefix="/")
login_manager = LoginManager(app)
app.register_blueprint(user_center_bp)

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Users'
container = database.get_container_client(CONTAINER_NAME)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.secret_key = "Mario" # necessary step for session
# app.register_blueprint(login_bp, url_prefix='/login')

@login_manager.user_loader
def load_user(username):
    user_email = list(container.query_items(
        query='SELECT Users.email FROM Users WHERE Users.email = @username',
        parameters=[dict(name="@username", value=username)], 
        enable_cross_partition_query=True))
    if not user_email:
        return None
    return User(email=user_email[0])

if __name__ == "__main__":
    app.run(debug=True)
