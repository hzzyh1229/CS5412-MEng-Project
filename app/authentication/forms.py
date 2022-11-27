"""
Sign-up & log-in forms.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
# from wtforms.validators import Required, Length, Email, Regexp, EqualTo
# from .. import models
from models import User
from azure.cosmos import CosmosClient
import requests 

API_BASE = "https://cs5412cloudjobboard.azurewebsites.net/"

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Users'
container = database.get_container_client(CONTAINER_NAME)

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    nickname = PasswordField('Nickname')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user_info = list(container.query_items(
            query='SELECT * FROM Users WHERE Users.email = @email', 
                parameters=[dict(name="@email", value=email.data)], 
                enable_cross_partition_query=True))
        # user_info = requests.get(API_BASE + f"users/{email}").json()
        if (len(user_info) > 0):
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                       Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email):
        user_info = list(container.query_items(
            query='SELECT * FROM Users WHERE Users.email = @email', 
                parameters=[dict(name="@email", value=email.data)], 
                enable_cross_partition_query=True))
        # user_info = requests.get(API_BASE + f"users/{email}").json()
        if (len(user_info) == 0):
            raise ValidationError('Email is not registered.')


class ForgetPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                       Email()])
    submit = SubmitField('Forget Password')