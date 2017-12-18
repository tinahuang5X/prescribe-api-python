from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from flask_restful import Resource, reqparse
import psycopg2
from config import config



from security import authenticate, identity, Token
from user import UserRegister, User
from item import Item, ItemList, ItemOther
from patient import Patient, PatientList, PatientOther

app = Flask(__name__)

app.secret_key = 'jose'
api = Api(app)
CORS(app)

jwt = JWT(app, authenticate, identity)


# api.add_resource(Item, '/item/<int:doctorId>')
@app.before_request

def log_request_info():

    app.logger.debug('Headers: %s', request.headers)

    app.logger.debug('Body: %s', request.get_data())


api.add_resource(Item, '/drugs/<int:doctorId>')
api.add_resource(ItemOther, '/drugs/<int:id>')
api.add_resource(ItemList, '/drugs')

api.add_resource(Patient, '/patients/<int:doctorId>')
api.add_resource(PatientOther, '/patients/<int:id>')
api.add_resource(PatientList, '/patients')


api.add_resource(UserRegister, '/doctors')

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

@app.route('/userId')
def make_payload():
    user_id = payload['identity']
    return {'user_id': user_id}


if __name__== '__main__':
    app.run(port=8000, debug=True)
