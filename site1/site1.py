import sqlite3
from flask import Flask, render_template
# To respond with a 404 page
from werkzeug.exceptions import abort
# from flask_caching import Cache

app = Flask(__name__)
# app.config.from_object('config.Config')
# cache = Cache(app)

@app.route('/')
# @cache.cached(timeout=30, query_string=True)
def hello():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# opens a connection to the database.db database file, and then 
# sets the row_factory attribute to sqlite3.Row so you can have 
# name-based access to columns.
# the database connection will return rows that behave like regular Python dictionaries
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
    
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')