from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from azure.cosmos import CosmosClient
from datetime import datetime

forum_bp = Blueprint('forum_bp', __name__, template_folder='templates')
URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

POSTS_CONTAINER_NAME = 'Posts'
posts_container = database.get_container_client(POSTS_CONTAINER_NAME)
COMMENTS_CONTAINER_NAME = 'Comments'
comment_container = database.get_container_client(COMMENTS_CONTAINER_NAME)

@forum_bp.route('/', methods=['GET', 'POST'])
def getAllPosts():
    """
    return all posts at the home page of forum
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login_bp.login'))

    posts_info = []
    if not session.get("post_data"):
        posts_info = list(posts_container.query_items(
        query='SELECT * FROM Posts', enable_cross_partition_query=True))
        session["post_data"] = posts_info
    else:
        posts_info = session["post_data"]
        
    # page num
    if not session.get("post_page"): 
        session["post_page"] = 0
    if request.method == "POST":
        #change pages
        if "changePage" in request.form.keys():
            if request.form["changePage"] == "next" and (session["post_page"]+1)*5 < len(posts_info):
                session["post_page"] += 1
            elif request.form["changePage"] == "previous" and session["post_page"] > 0:
                session["post_page"] -= 1
            print("cur_page is : ",session["post_page"]+1)
    
    n_results = len(session["post_data"])
    data = session["post_data"][session["post_page"]*5: session["post_page"]*5+5]
    info = {}
    info["posts"] = data
    info["post_page"] = session["post_page"] + 1
    info["num_results"] = n_results
    return render_template("forum.html", info = info)

@forum_bp.route('/createPost', methods=['GET', 'POST'])
def createPost():
    """
    create a post
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login_bp.login'))
    if request.method == 'POST':
        title = request.form['title']
        print(title)
        content = request.form['content']
        company = request.form['company']
        postOwner = current_user.get_username()['email']
        time = datetime.today().strftime('%Y%m%d%H%M')
        print(time)
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            posts_container.upsert_item({"title": title, "company": company,
                "postOwner": postOwner, "numOfComments": 1, "time": time})
            comment_container.upsert_item({'postId': postOwner+title, 'user': postOwner, 
                'content': content, 'time': time})
            session["post_data"] = list(posts_container.query_items(query='SELECT * FROM Posts', enable_cross_partition_query=True))
        return redirect(url_for('forum_bp.getAllPosts'))
    return render_template("create_post.html")
