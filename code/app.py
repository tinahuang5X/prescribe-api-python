from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)

app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)


# api.add_resource(Item, '/item/<int:doctorId>')
api.add_resource(Item, '/drugs/<int:id>')
api.add_resource(ItemList, '/drugs')
api.add_resource(UserRegister, '/register')

if __name__== '__main__':
    app.run(port=8000, debug=True)
