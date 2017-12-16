from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from flask_restful import Resource, reqparse
import psycopg2
from config import config




from security import authenticate, identity
from user import UserRegister, User
from item import Item, ItemList, ItemOther

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
api.add_resource(UserRegister, '/register')




if __name__== '__main__':
    app.run(port=8000, debug=True)
