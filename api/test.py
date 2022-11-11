import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "jobs")
# print(response.json())

# response = requests.get(BASE + "jobs/3335078381")
# print(response.json())
import json

f = open('LinkedIn202210281807.json')
    
# returns JSON object as 
# a dictionary
data = json.load(f)
for job in data[100:110]:
    response = requests.put(BASE + f'jobs/{job["job_id"]}', job)

    
