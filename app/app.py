from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from authentication.authentication import login_bp
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(login_bp)
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# app.register_blueprint(login_bp, url_prefix='/login')

@app.route('/')
def index():
    """
    place holder
    """
    # return render_template('login.html')
    return "main page"