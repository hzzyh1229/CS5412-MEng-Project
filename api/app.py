from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

import os
from azure.cosmos import CosmosClient
import numpy as np
from numpy.linalg import norm

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Positions'
job_container = database.get_container_client(CONTAINER_NAME)

CONTAINER_NAME = 'Applications'
application_container = database.get_container_client(CONTAINER_NAME)

CONTAINER_NAME = 'Users'
user_container = database.get_container_client(CONTAINER_NAME)

CONTAINER_NAME = 'Comments'
comment_container = database.get_container_client(CONTAINER_NAME)

CONTAINER_NAME = 'Posts'
post_container = database.get_container_client(CONTAINER_NAME)

class Job(Resource):
    def get(self, job_id):
        data = list(job_container.query_items(
        query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
        enable_cross_partition_query=True))
        return data

    def put(self, job_id):
        job = request.form
        print(job_id)
        temp = list(job_container.query_items(query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"', enable_cross_partition_query=True))
        if(len(temp) == 0):
            job_container.upsert_item(job)
        else:
            print("already existed")

class CompanyJob(Resource):
    def get(self, company):
        data = list(job_container.query_items(
        query=f'SELECT * FROM c where c.company = "{company}"',
        enable_cross_partition_query=True))
        return data


class AllJob(Resource):
    def get(self):
        data = list(job_container.query_items(
        query='SELECT * FROM c',
        enable_cross_partition_query=True))
        return data

api.add_resource(AllJob, "/jobs")
api.add_resource(Job, "/jobs/<string:job_id>")
api.add_resource(CompanyJob, "/jobs/company=<string:company>")


# input is user email, recommend jobs for this user
class RecommendJob(Resource):
    def get(self, email):

        # email = "test1@gmail.com"
        all_jobs = list(job_container.query_items(
        query='SELECT * FROM c',
        enable_cross_partition_query=True))

        past_applications = list(application_container.query_items(
            query= f'SELECT * FROM c WHERE c.email = "{email}"',
            enable_cross_partition_query=True))
        if len(past_applications) == 0:
            return all_jobs[:10]
        # first getting the mean vec of this person
        applicant_vec = np.array([0.0] * 96)
        for application in past_applications:
            job_id = application["job_id"]
            job_vec = list(job_container.query_items(
            query= f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
            enable_cross_partition_query=True))[0]["word_vec"]
            applicant_vec += np.array(job_vec)
        applicant_vec /= len(past_applications)

        top_data = []

        for job in all_jobs:
            job_vec = job["word_vec"]
            cosine = np.dot(applicant_vec, job_vec)/(norm(applicant_vec)*norm(job_vec))
            top_data.append([cosine, job])

        top_data.sort(reverse=True, key=lambda x: x[0])
        top_data = top_data[:10]
        recommended_jobs = []
        for data in top_data:
            recommended_jobs.append(data[1])

        return recommended_jobs

api.add_resource(RecommendJob, "/jobs/recommend/<string:email>")

# get and post for applicatoin
# only have email or both have email and job_id
# if job_id is not provided, replace with null
class Application(Resource):
    def get(self, job_id, email, status):
        if job_id == 'null':
            data = list(application_container.query_items(
            query= f'SELECT * FROM c WHERE c.email = "{email}"',
            enable_cross_partition_query=True))
            return data
        elif email == 'null':
            data = list(application_container.query_items(
            query= f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
            enable_cross_partition_query=True))
            return data
        else:
            data = list(application_container.query_items(
            query= f'SELECT * FROM c WHERE c.job_id = "{job_id}" AND c.email = "{email}"',
            enable_cross_partition_query=True))
            return data

    def put(self, job_id, email, status):
        application_container.upsert_item({"email": email, 
                        "job_id": job_id, "status": status})

api.add_resource(Application, "/applications/<string:job_id>/<string:email>/<string:status>")

class DeleteApplication(Resource):
    def put(self, email, job_id):
        print(email)
        for item in application_container.query_items(
        query=f'SELECT * FROM Applications WHERE Applications.job_id = @id AND Applications.email = "{email}"',
        parameters=[dict(name="@id", value=job_id)],
        enable_cross_partition_query=True):
            print(item["email"])
            application_container.delete_item(item["id"], partition_key=email)

api.add_resource(DeleteApplication, "/delete/applications/<string:job_id>/<string:email>")

class User(Resource):
    def get(self, email):
        data = list(user_container.query_items(
            query='SELECT * FROM Users WHERE Users.email = @email', 
                parameters=[dict(name="@email", value=email)], 
                enable_cross_partition_query=True))
        return data


api.add_resource(User, "/users/<string:email>")

class UserEmail(Resource):
    def get(self, email):
        data = list(user_container.query_items(
        query='SELECT Users.email FROM Users WHERE Users.email = @username',
        parameters=[dict(name="@username", value=email)], 
        enable_cross_partition_query=True))
        return data


api.add_resource(UserEmail, "/users/email/<string:email>")


if __name__ == "__main__":
    app.run()
