import sqlite3
from flask_restful import Resource, reqparse
import psycopg2
from config import config
import bcrypt

class User(object):
    def __init__(self, _id, firstName, lastName, username, password, hashed_password):
        # import pdb; pdb.set_trace()
        self.id = _id
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        # self.password = password
        self.password = password.encode('utf-8')
        self.hashed_password = bcrypt.hashpw(self.password, bcrypt.gensalt(10)).decode('utf-8')

    @classmethod
    def find_by_username(cls, username):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()


        query = "SELECT * FROM doctor WHERE username=%s"
        cur.execute(query, (username,))
        row = cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user
    @classmethod
    def find_by_id(cls, _id):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "SELECT * FROM doctor WHERE id=%s"

        cur.execute(query, (_id,))
        row = cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user

class UserRegister(Resource):


    parser = reqparse.RequestParser()

    parser.add_argument('firstName',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('lastName',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['email']):
            return {"message": "User with that username already exists."}, 400

        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = """
        INSERT INTO doctor (firstName, lastName, username, password)
        VALUES ('{first_name}', '{last_name}', '{username}', '{password}'); """.format(first_name=data['firstName'], last_name=data['lastName'],
        username=data['email'], password=data['password'] )


        cur.execute(query)


        # query = "INSERT INTO doctor VALUES (NULL, %s, %s, %s, %s)"
        #
        # cur.execute(query, (data['firstName'], data['lastName'], data['username'], data['password']))

        conn.commit()

        conn.close()

        return {"message": "Doctor created successfully"}, 201
