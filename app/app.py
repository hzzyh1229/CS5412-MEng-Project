from flask import Flask, redirect, url_for, render_template, request, session, flash
from home.home import home

app = Flask(__name__)

app.register_blueprint(home, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
