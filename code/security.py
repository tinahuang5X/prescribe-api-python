from werkzeug.security import safe_str_cmp
from flask_jwt import JWT, jwt_required, current_identity

from user import User
from flask_restful import Resource, reqparse
import psycopg2
from config import config
from user import UserRegister
import logging
import bcrypt


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        logging.warning("password comparison success")
        return user
    else:
        logging.warning(user, user.password, password, "login failure")
        return None

# def authenticate(username, password):
#     user = User.find_by_username(username)
#     if user and safe_str_cmp(user.password, password):
#         logging.warning("password comparison success")
#         return user
#     else:
#         logging.warning(user, user.password, password, "login failure")
#         return 400
#

def identity(payload):
    user_id = payload['identity']
    print('>>>>>> %s', user_id)
    return User.find_by_id(user_id)



# def _custom_default_auth_response_handler(access_token, identity):
#     return jsonify({'id': identity.id, 'access_token': access_token.decode('utf-8')})

# jwt.auth_request_callback = _custom_default_auth_response_handler
