from werkzeug.security import safe_str_cmp
from user import User
from flask_restful import Resource, reqparse
import psycopg2
from config import config
from user import UserRegister
import logging



# def authenticate(username, hashedPassword):
#     user = User.find_by_username(username)
#     if user and safe_str_cmp(user.hashedPassword, hashedPassword):
#         logging.warning("password comparison success")
#         return user
#     else:
#         logging.warning(user, user.hashedPassword, hashedPassword, "login failure")
#
# def identity(payload):
#     user_id = payload['identity']
#     return User.find_by_id(user_id)


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        logging.warning("password comparison success")
        return user
    else:
        logging.warning(user, user.password, password, "login failure")

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

# from werkzeug.security import safe_str_cmp
# from user import User
#
# def authenticate(username, password):
#     user = User.find_by_username(username)
#     if user and safe_str_cmp(user.password, password):
#         return user
#
# def identity(payload):
#     user_id = payload['identity']
#     return User.find_by_id(user_id)
