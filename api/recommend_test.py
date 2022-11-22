from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

import os
import numpy as np
from numpy.linalg import norm

from azure.cosmos import CosmosClient

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


email = "test1@gmail.com"
all_jobs = list(job_container.query_items(
query='SELECT * FROM c',
enable_cross_partition_query=True))

past_applications = list(application_container.query_items(
    query= f'SELECT * FROM c WHERE c.email = "{email}"',
    enable_cross_partition_query=True))

# first getting the mean vec of this person
applicant_vec = np.array([0.0] * 96)
for application in past_applications:
    job_id = application["job_id"]
    job_vec = list(job_container.query_items(
    query= f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
    enable_cross_partition_query=True))[0]["word_vec"]
    applicant_vec += np.array(job_vec)
applicant_vec /= len(past_applications)
#print(applicant_vec)

# iterating through all jobs to find top ones
top_data = []

i = 0
for job in all_jobs:
    #print("i is: ",i)
    # print(job["job_id"])
    i += 1
    job_vec = job["word_vec"]
    cosine = np.dot(applicant_vec, job_vec)/(norm(applicant_vec)*norm(job_vec))
    #print("Job", job["position"], "Cosine Similarity:", cosine)
    top_data.append([cosine, job])

top_data.sort(reverse=True, key=lambda x: x[0])
top_data = top_data[:10]
recommended_jobs = []
for data in top_data:
    recommended_jobs.append(data[1])

