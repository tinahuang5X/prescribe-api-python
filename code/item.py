from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
import psycopg2
from config import config

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('generic', type=str)
    parser.add_argument('brand', type=str)
    parser.add_argument('indications', type=str)
    parser.add_argument('doctorId', type=int)

    # @jwt_required()
    def get(self, doctorId):
        item = self.find_by_doctorId(doctorId)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_doctorId(cls, doctorId):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE doctorId=?"
        result = cursor.execute(query, (doctorId,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'id': row[0], 'doctorId': row[1], 'generic': row[2], 'brand': row[3], 'indications': row[4]}}

    def post(self, doctorId):

        if self.find_by_doctorId(doctorId):
            # return {'message': "An item with generic '{}' already exists.".format(generic)}, 400
            data = Item.parser.parse_args()

            item = {'id': data['id'], 'doctorId': doctorId, 'generic': data['generic'], 'brand': data['brand'],'indications': data['indications']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500


        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?, ?, ?, ?)"
        cursor.execute(query, (item['id'], item['generic'], item['brand'], item['indications'], item['doctorId']))

        connection.commit()
        connection.close()

    # @jwt_required()
    def delete(self, id):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "DELETE FROM Drug WHERE id=%s"
        cur.execute(query, (id,))

        conn.commit()
        cur.close()
        conn.close()
        return {'message': 'Item deleted'}

    # @jwt_required()
    @classmethod
    def find_by_id(cls, id):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "SELECT * FROM Drug WHERE id=%s"
        cur.execute(query, (id,))
        drug = cur.fetchone()
        conn.close()

        if drug:
            print(drug)
            return {'drug': {'id': drug[0], 'generic': drug[1], 'brand': drug[2], 'indications': drug[3], 'doctorId': drug[4]}}

    def patch(self, id):
        data = Item.parser.parse_args()
        item = self.find_by_id(id)
        print(item)
        updated_item = {'id': id, 'generic': data['generic'], 'brand': data['brand'], 'indications': data['indications'], 'doctorId': data['doctorId']}
        print(updated_item)
        try:
            self.update(updated_item)
        except:

            return {"message": "An error occurred updating the item."}, 500
        return updated_item


    @classmethod
    def update(cls,item):
        conn = None

        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        if generic:
            query = "UPDATE Drug SET generic=%s WHERE id=%s"
            cur.execute(query, (item['generic']))
        if brand:
            query = "UPDATE Drug SET brand=%s WHERE id=%s"
            cur.execute(query, (item['brand']))
        if indications:
            query = "UPDATE Drug SET indications=%s WHERE id=%s"
            cur.execute(query, (item['indications']))



        # query = "UPDATE Drug SET generic=%s, brand=%s, indications=%s, doctorId=%s WHERE id=%s"
        #
        # cur.execute(query, (item['generic'], item['brand'], item['indications'], item['doctorId'], item['id']))


        conn.commit()

        cur.close()
        conn.close()



class ItemList(Resource):
    # @jwt_required()
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "SELECT * FROM Drug"
        cur.execute(query)
        #import pdb; pdb.set_trace()
        drugs = []
        for row in cur:
            drugs.append({'id': row[0], 'generic': row[1], 'brand': row[2], 'indications': row[3], 'doctorId': row[4] })

            # connection.close()
        cur.close()
        conn.close()

        return {'drugs': drugs}
