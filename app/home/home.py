from azure.cosmos import CosmosClient
from multiprocessing import JoinableQueue
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from requests import request
from datetime import datetime
import requests
from flask import Flask, redirect, url_for, render_template, Blueprint, session, request, flash
from cache import cache
home_bp = Blueprint("home", __name__, static_folder="static",  static_url_path='/static/home', template_folder="templates")

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Positions'
container = database.get_container_client(CONTAINER_NAME)
CONTAINER_NAME2 = 'Applications'
application_container = database.get_container_client(CONTAINER_NAME2)

API_BASE = "https://cs5412cloudjobboard.azurewebsites.net/"

@home_bp.route("/", methods = ["POST", "GET"])
def home():
    jobs_info = []
    if not session.get("page"): 
        session["page"] = 0
    if not session.get("data"):
        # jobs_info = list(container.query_items(
        # query='SELECT * FROM c',
        # enable_cross_partition_query=True))
        # session["data"] = jobs_info
        jobs_info = requests.get(API_BASE + 'jobs').json()
        session["data"] = jobs_info
    else:
        jobs_info = session["data"]

    error = None
    error_job_id = None
    if request.method == "POST":
        #change pages
        if "changePage" in request.form.keys():
            if request.form["changePage"] == "next" and (session["page"]+1)*5 < len(jobs_info):
                session["page"] += 1
            elif request.form["changePage"] == "last" and session["page"] > 0:
                session["page"] -= 1
        #print("cur_page is : ",session["page"]+1)
    
        #apply job
        elif "apply" in request.form.keys():
            if not current_user.is_authenticated:
                return redirect(url_for('login_bp.login'))
            if (request.form["apply"]):
                job_id = request.form["apply"]
                user_email = current_user.get_username()['email']
                cur_date = datetime.today().strftime('%Y/%m/%d')
                # application_info = list(application_container.query_items(
                #     query='SELECT * FROM c WHERE c.job_id = @job_id AND c.email = @email', 
                #     parameters=[dict(name = "@job_id", value = job_id), dict(name="@email", value=user_email)], 
                #     enable_cross_partition_query=True))
                application_info = requests.get(API_BASE + f"/applications/{job_id}/{user_email}/any").json()
                if (len(application_info) == 0):
                    application_container.upsert_item({"email":user_email, "job_id": job_id, 
                    "status": "submitted", "apply_date": cur_date, "oa_vo_date": "N/A", 
                    "offer_date": "N/A", "reject_date": "N/A"})

                else:
                    error = 'you have already applied for this job'
                    error_job_id = job_id
                    print("application already exist")

        elif "filter" in request.form.keys():
            company = request.form["company"]
        #     session["data"] = list(container.query_items(
        # query=f'SELECT * FROM c where c.company = "{company}"',
        # enable_cross_partition_query=True))
            if company == "":
                session["data"] = requests.get(API_BASE + f"/jobs").json()
            else:
                session["data"] = requests.get(API_BASE + f"/jobs/company={company}").json()
        #print("cur_page is : ",session["page"]+1)
        elif "recommend" in request.form.keys():
            if not current_user.is_authenticated:
                return redirect(url_for('login_bp.login'))
            flash('Here are the recommended jobs for you!')
            user_email = current_user.get_username()['email']
            session["data"] = requests.get(API_BASE + f"/jobs/recommend/{user_email}").json()

    n_results = len(session["data"])
    data = session["data"][session["page"]*5: session["page"]*5+5]
    info = {}
    info["jobs"] = data
    info["page"] = session["page"] + 1
    info["n_results"] = n_results
    return render_template("home.html", info = info, error = error, error_job_id = error_job_id)

@home_bp.route("/job<job_id>")
@cache.cached(timeout=60)
def position(job_id):
    #job_info = list(container.query_items(query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"', enable_cross_partition_query=True))[0]
    job_info = requests.get(API_BASE + f"jobs/{job_id}").json()[0]
    return render_template("job_description.html", job_info = job_info)
