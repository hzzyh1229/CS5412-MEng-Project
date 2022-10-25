import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

from . import app

# @app.route('/')
# def main():
#     return render_template('/home.html')
#     # return 'This is the main page.'

# def get_db_connection():
#     """
#     opens a connection to the database & get name-based access to columns in python dict form
#     """
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn


# def get_job_helper(job_id):
#     """
#     get the job info
#     """
#     conn = get_db_connection()
#     job = conn.execute('SELECT * FROM jobs WHERE id = ?',
#                         (job_id,)).fetchone()
#     conn.close()
#     if job is None:
#         abort(404)
#     return job

# @app.route('/<int:job_id>')
# def get_job(job_id):
#     """
#     return the page corresponds to the job id
#     """
#     job = get_job_helper(job_id)
#     return render_template('job.html', job=job)

# @app.route('/login')
# def log_in():
#     """
#     return the login page
#     """
#     # return render_template('login.html')
#     raise Exception("Not Implemented")

# @app.route('/logout')
# def log_out():
#     """
#     return the logout page
#     """
#     raise Exception("Not Implemented")

# @app.route('/profile')
# def profile():
#     """
#     return the profile page
#     """
#     raise Exception("Not Implemented")



    
# if __name__ == '__main__':
# 	app.run(debug=True, host='0.0.0.0')