from multiprocessing import JoinableQueue
from flask import Flask, redirect, url_for, render_template, Blueprint
from azure.cosmos import CosmosClient

home_bp = Blueprint("home", __name__, static_folder="static",  static_url_path='/static/home', template_folder="templates")

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'users'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'users1'
container = database.get_container_client(CONTAINER_NAME)


@home_bp.route("/")
def home():
    data = container.query_items(
            query='SELECT * FROM c',
            enable_cross_partition_query=True)

    return render_template("home.html", jobs = data)

