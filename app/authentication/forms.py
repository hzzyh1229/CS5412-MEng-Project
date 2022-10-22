"""
Sign-up & log-in forms.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
# from wtforms.validators import Required, Length, Email, Regexp, EqualTo
# from .. import models
from models import User

class RegistrationForm(FlaskForm):
    # email = StringField('Email', 
    #                     validators=[Required(), Length(1, 64), Email()])
    # password = PasswordField('Password', 
    #                         validators=[ 
    #                             Required(), 
    #                             EqualTo('password2', message='Passwords must match.')])
    # password2 = PasswordField('Confirm password', validators=[Required()])
    # submit = SubmitField('Register')

    # def validate_email(self, field):
    #     if models.User.email_is_registered(field.data):
    #         raise ValidationError('Email already registered.')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    # email = StringField(
    #     'Email',
    #     validators=[
    #         DataRequired(),
    #         Email(message='Enter a valid email.')
    #     ]
    # )
    # password = PasswordField('Password', validators=[DataRequired()])
    # submit = SubmitField('Log In')
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                       Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ForgetPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                       Email()])
    submit = SubmitField('Forget Password')