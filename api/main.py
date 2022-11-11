from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


from azure.cosmos import CosmosClient

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Positions'
job_container = database.get_container_client(CONTAINER_NAME)

class Job(Resource):
    def get(self, job_id):
        data = list(job_container.query_items(
        query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
        enable_cross_partition_query=True))
        return data[0]

    def put(self, job_id):
        job = request.form
        print(job_id)
        temp = list(job_container.query_items(query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"', enable_cross_partition_query=True))
        if(len(temp) == 0):
            job_container.upsert_item(job)
        else:
            print("already existed")

class AllJob(Resource):
    def get(self):
        data = list(job_container.query_items(
        query='SELECT * FROM c',
        enable_cross_partition_query=True))
        return data[:10]

api.add_resource(AllJob, "/jobs")
api.add_resource(Job, "/jobs/<string:job_id>")

if __name__ == "__main__":
	app.run(debug=True)