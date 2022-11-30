from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from azure.cosmos import CosmosClient
from datetime import datetime
from cache import cache

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
@cache.cached(timeout=60)
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

def getTime():
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

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
        time = getTime()
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

@forum_bp.route("/<post_owner>/<title>")
def post(post_owner, title):
    post_info = list(posts_container.query_items(query=f'SELECT * FROM posts WHERE posts.title = "{title}" AND posts.postOwner = "{post_owner}"', enable_cross_partition_query=True))[0]
    print("post_info: ")
    print(post_info["title"])
    comments_info = list(comment_container.query_items(query=f'SELECT * FROM c WHERE c.postId = "{post_owner+title}"', enable_cross_partition_query=True))
    return render_template("post_description.html", post_info = post_info, comments_info = comments_info)

@forum_bp.route('/create_comment/<title>/<post_owner>', methods=['GET', 'POST'])
def createComment(title, post_owner):
    """
    create a comment
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login_bp.login'))
    if request.method == 'POST':
        content = request.form['content']
        user = current_user.get_username()['email']
        time = datetime.today().strftime('%Y%m%d%H%M')
        if not content:
            flash('Content is required!')
        else:
            comment_container.upsert_item({'postId': post_owner+title, 'user': user, 
                'content': content, 'time': time})
        return redirect(url_for('forum_bp.post', post_owner=post_owner, title=title))
    return render_template("create_comment.html")