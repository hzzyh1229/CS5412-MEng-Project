import requests

BASE = "http://127.0.0.1:5000/"
BASE = "https://cs5412cloudjobboard.azurewebsites.net/"
# response = requests.get(BASE + "jobs")
# print(response.json())

# response = requests.get(BASE + "jobs/3335078381")
# print(response.json())
import json

#f = open('LinkedIn202210281807.json')
    
# returns JSON object as 
# a dictionary


# class Job(Resource):
#     def get(self, job_id):
#         data = list(job_container.query_items(
#         query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
#         enable_cross_partition_query=True))
#         return data[0]

#     def put(self, job_id):
#         job = request.form
#         print(job_id)
#         temp = list(job_container.query_items(query=f'SELECT * FROM c WHERE c.job_id = "{job_id}"', enable_cross_partition_query=True))
#         if(len(temp) == 0):
#             job_container.upsert_item(job)
#         else:
#             print("already existed")
# api.add_resource(Job, "/jobs/<string:job_id>")
#response = requests.get(BASE + f'jobs/3318270727')

# data = json.load(f)
# for job in data[130:131]:
#     response = requests.put(BASE + f'jobs/{job["job_id"]}', job)
    

# class CompanyJob(Resource):
#     def get(self, company):
#         data = list(job_container.query_items(
#         query=f'SELECT * FROM c where c.company = "{company}"',
#         enable_cross_partition_query=True))
#         return data
# api.add_resource(CompanyJob, "/jobs/company=<string:company>")
#response = requests.get(BASE + f'jobs/company=Apple')

# class AllJob(Resource):
#     def get(self):
#         data = list(job_container.query_items(
#         query='SELECT * FROM c',
#         enable_cross_partition_query=True))
#         return data[:10]
# api.add_resource(AllJob, "/jobs")
#response = requests.get(BASE + f'jobs')


# # get and post for applicatoin
# # only have email or both have email and job_id
# # if job_id is not provided, replace with null
# class Application(Resource):
#     def get(self, job_id, email, status):
#         if job_id == 'null':
#             data = list(application_container.query_items(
#             query= f'SELECT * FROM c WHERE c.email = "{email}"',
#             enable_cross_partition_query=True))
#             return data
#         elif email == 'null':
#             data = list(application_container.query_items(
#             query= f'SELECT * FROM c WHERE c.job_id = "{job_id}"',
#             enable_cross_partition_query=True))
#             return data
#         else:
#             data = list(application_container.query_items(
#             query= f'SELECT * FROM c WHERE c.job_id = "{job_id}" AND c.email = "{email}"',
#             enable_cross_partition_query=True))
#             return data

#     def put(self, job_id, email, status):
#         application_container.upsert_item({"email": email, 
#                         "job_id": job_id, "status": status})

# api.add_resource(Application, "/applications/<string:job_id>/<string:email>/<string:status>")


response = requests.get(BASE + 'applications/null/test1@gmail.com/null')
response = requests.get(BASE + 'applications/3335080633/test1@gmail.com/null')
response = requests.get(BASE + 'applications/3335080633/null/null')
print(response.json())
#response = requests.put(BASE + 'applications/3335080633/test1@gmail.com/submitted')


# class DeleteApplication(Resource):
#     def put(self, email, job_id):
#         for item in application_container.query_items(
#         query='SELECT * FROM Applications WHERE Applications.job_id = @id',
#         parameters=[dict(name="@id", value=job_id)],
#         enable_cross_partition_query=True):
#           application_container.delete_item(item, partition_key=email)

# api.add_resource(DeleteApplication, "/delete/applications/<string:job_id>/<string:email>")
#response = requests.put(BASE + '/delete/applications/3335080633/test1@gmail.com')


# class User(Resource):
#     def get(self, email):
#         data = list(user_container.query_items(
#             query='SELECT * FROM Users WHERE Users.email = @email', 
#                 parameters=[dict(name="@email", value=email)], 
#                 enable_cross_partition_query=True))
#         return data


# api.add_resource(User, "/users/<string:email>")
#response = requests.get(BASE + 'users/test1@gmail.com')
