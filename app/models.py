# from . import app, login_manager
from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    # id = ''
    # email = ''
    # password_hash = ''
    # confirmed = False

    def __init__(self, username, email, password=None, password_hash=None):
        self.username = username
        self.email = email
        if password_hash:
            self.password_hash = password_hash
        else:
            self.password_hash = generate_password_hash(password)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def email_is_registered(email):
        return User.find_by_email(email) is not None

    # def __repr__(self):
    #     return '<User %r>' % self.email

    # def save(self):

    #     if self.id != None:
    #         raise BaseException("Updating user account is not supported")

    #     user_id = UserDAO.create_user(
    #                                 self.email,
    #                                 self.password_hash
    #                                 )
    #     self.user_id = id

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

    
