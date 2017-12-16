
from flask_restful import Resource, reqparse
import psycopg2
from config import config



class User(Resource):
    def __init__(self, _id, firstName, lastName, username, hashedPassword):
        # import pdb; pdb.set_trace()
        self.id = _id
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.hashedPassword = hashedPassword

    @classmethod
    def find_by_username(cls, username):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "SELECT * FROM doctor WHERE username=%s"
        print(query)
        print(cur.execute(query, (username,)))
        row = cur.fetchone()

        if row:
            user = cls(*row)
            print('1st', user)
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
            print('2nd', user)
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
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('hashedPassword',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        print('hi', data)

        if User.find_by_username(data['username']):
            print(data['username'])
            return {"message": "User with that username already exists."}, 400

        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = """
        INSERT INTO doctor (firstName, lastName, username, hashedPassword)
        VALUES ('{first_name}', '{last_name}', '{username}', '{hashedPassword}'); """.format(first_name=data['firstName'], last_name=data['lastName'],
        username=data['username'], hashedPassword=data['hashedPassword'] )

        # query = "INSERT INTO doctor VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query)
        conn.commit()



        conn.close()

        return {"message": "User created successfully"}, 201
