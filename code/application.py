from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from flask_restful import Resource, reqparse
import psycopg2
from config import config
import os
endpoint = os.environ['API_ENDPOINT']


from security import authenticate, identity
from user import UserRegister, User
from item import Item, ItemList, ItemOther
from patient import Patient, PatientList, PatientOther

application = Flask(__name__)

application.secret_key = 'jose'
api = Api(application)
CORS(application)

jwt = JWT(application, authenticate, identity)



# api.add_resource(Item, '/item/<int:doctorId>')
@application.before_request

def log_request_info():

    application.logger.debug('Headers: %s', request.headers)

    application.logger.debug('Body: %s', request.get_data())


api.add_resource(Item, '/drugs/<int:doctorId>')
api.add_resource(ItemOther, '/drugs/<int:id>')
api.add_resource(ItemList, '/doctors/<int:doctorId>/drugs')

api.add_resource(Patient, '/patients/<int:doctorId>')
api.add_resource(PatientOther, '/patients/<int:id>')
api.add_resource(PatientList, '/doctors/<int:doctorId>/patients')


api.add_resource(UserRegister, '/doctors')







if __name__== '__main__':
    application.run(port=8000, debug=True)
