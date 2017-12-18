from werkzeug.security import safe_str_cmp
from flask_jwt import JWT, jwt_required, current_identity
from user import User
from flask_restful import Resource, reqparse
import psycopg2
from config import config
from user import UserRegister
import logging


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


def make_payload(identity):
    return {'user_id': identity.id}

class Token(object):

    def __init__(self, access_token, identity):
        # import pdb; pdb.set_trace()
        self.access_token = access_token
        self.identity = identity

    @classmethod
    def auth_response(cls, access_token, identity):
        return jsonify({'access_token': access_token.decode('utf-8'), 'userId': identity.id})
