from azure.cosmos import CosmosClient

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Users'
container = database.get_container_client(CONTAINER_NAME)

def main():
    container.upsert_item({"email": "tempp@email.com", "password": "12345", "name": "Mario"})

if __name__ == "__main__":
    main()