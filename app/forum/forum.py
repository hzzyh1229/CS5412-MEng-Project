from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from azure.cosmos import CosmosClient

forum_bp = Blueprint('forum_bp', __name__, template_folder='templates')
URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Posts'
posts_container = database.get_container_client(CONTAINER_NAME)

@forum_bp.route('/', methods=['GET', 'POST'])
def getAllPosts():
    """
    return all posts at the home page of forum
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home.home'))
    if not session.get("post_page"): 
        session["post_page"] = 0
    if not session.get("post_data"):
        session["post_data"] = list(posts_container.query_items(
        query='SELECT * FROM Posts', enable_cross_partition_query=True))
    n_results = len(session["post_data"])
    data = session["post_data"][session["post_page"]*5: session["post_page"]*5+5]
    info = {}
    info["posts"] = data
    info["post_page"] = session["post_page"] + 1
    info["num_results"] = n_results
    return render_template("forum.html", info = info)
