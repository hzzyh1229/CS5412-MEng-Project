from flask import Blueprint, render_template

home = Blueprint("home", __name__, template_folder="templates")

@home.route("/")
def home():
    return "<h1>Home Page </h1>"

