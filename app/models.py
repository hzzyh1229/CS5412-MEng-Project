from flask import Flask
from distutils.log import Log
from flask_login import UserMixin, AnonymousUserMixin, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from azure.cosmos import CosmosClient
# from app import login_manager
# from flask import current_app as app

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)
# login_manager = LoginManager(app)

CONTAINER_NAME = 'Users'
container = database.get_container_client(CONTAINER_NAME)



class User(UserMixin):

    def __init__(self, email, password=None, password_hash=None, nickname=None):
        self.username = email
        if password_hash:
            self.password_hash = password_hash
        elif password:
            self.password_hash = generate_password_hash(password)
        # else:

        if nickname:
            self.nickname = nickname
        else:
            self.nickname = 'User'

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_username(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    def save(self):
        container.upsert_item({"email":str(self.username), 
            "password":str(self.password_hash), "name":str(self.nickname)})

    @staticmethod
    def get_hashed(password):
        return generate_password_hash(password)

    def get_id(self):
        return self.username
    
    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)


    # @staticmethod
    # def email_is_registered(email):
    #     return User.find_by_email(email) is not None

    # def __repr__(self):
    #     return '<User %r>' % self.email

    # def save(self):
        
        # if self.username != None:
        #     raise BaseException("Updating user account is not supported")

        # user_id = UserDAO.create_user(
        #                             self.email,
        #                             self.password_hash
        #                             )
        # self.user_id = id

    # @staticmethod
    # def find_by_email(email):

    #     user_dict = UserDAO.find_by_email(email)

    #     if user_dict:
    #         return User(
    #                     user_dict['user_id'],
    #                     email,
    #                     password_hash=user_dict['password_hash']
    #                 )
    #     else:
    #         return None

    
