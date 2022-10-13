from flask import request, Flask, render_template
import json
from flask_caching import Cache
import time

app = Flask(__name__)
app.config.from_object('config.Config')
cache = Cache(app)

@app.route('/')
@cache.cached(timeout=30, query_string=True)

def hello_world():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
