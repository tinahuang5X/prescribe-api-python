from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import sqlite3
import psycopg2
from config import config
import json

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
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "SELECT * FROM Drug WHERE doctorId=%s"
        cur.execute(query, (doctorId,))
        drug = cur.fetchone()
        conn.close()

        if drug:
            print(drug)
            return {'drug': {'id': drug[0], 'generic': drug[1], 'brand': drug[2], 'indications': drug[3], 'doctorId': drug[4] }}




class ItemOther(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('generic', type=str)
    parser.add_argument('brand', type=str)
    parser.add_argument('indications', type=str)
    parser.add_argument('doctorId', type=int)
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
            print('1st', drug)
            return {'drug': {'id': drug[0], 'generic': drug[1], 'brand': drug[2], 'indications': drug[3], 'doctorId': drug[4]}}

    def patch(self, id):
        data = ItemOther.parser.parse_args()
        print("100", data)
        item = self.find_by_id(id)
        print('2nd', item)
        updated_item = {'id': id, 'generic': data['generic'], 'brand': data['brand'], 'indications': data['indications'], 'doctorId': data['doctorId']}
        print('3rd', updated_item)
        try:
            self.update(updated_item)

        except:

            return {"message": "An error occurred updating the item."}, 500
        return updated_item


    @classmethod
    def update(cls,item):
        data = Item.parser.parse_args()
        conn = None

        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        if data['generic']:
            query = "UPDATE Drug SET generic=%s WHERE id=%s"
            cur.execute(query, (item['generic'], item['id']))

        if data['brand']:
            query = "UPDATE Drug SET brand=%s WHERE id=%s"
            cur.execute(query, (item['brand'], item['id']))

        if data['indications']:
            query = "UPDATE Drug SET indications=%s WHERE id=%s"
            cur.execute(query, (item['indications'], item['id']))

        if data['doctorId']:
            query = "UPDATE Drug SET doctorId=%s WHERE id=%s"
            cur.execute(query, (item['doctorId'], item['id']))



        # query = "UPDATE Drug SET generic=%s, brand=%s, indications=%s, doctorId=%s WHERE id=%s"
        #
        # cur.execute(query, (item['generic'], item['brand'], item['indications'], item['doctorId'], item['id']))


        conn.commit()

        cur.close()
        conn.close()

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

class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('generic', type=str)
    parser.add_argument('brand', type=str)
    parser.add_argument('indications', type=str)
    parser.add_argument('doctorId', type=int)

    @jwt_required()
    def post(self, doctorId):

        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "SELECT MAX(id) from Drug"
        cur.execute(query)
        maxid = cur.fetchone()[0]

        # if self.find_by_doctorId(doctorId):
            # return {'message': "An item with generic '{}' already exists.".format(generic)}, 400
        data = ItemList.parser.parse_args()
        print("hi", data)

        created_item = {'id': maxid+1, 'doctorId': doctorId, 'generic': data['generic'], 'brand': data['brand'],'indications': data['indications']}
        print("hello", created_item)

        try:
            ItemList.insert(created_item)
        # except:
        #     return {"message": "An error occurred inserting the item."}, 500
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return created_item, 201

    @classmethod
    def insert(cls, item):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "INSERT INTO Drug VALUES(%s, %s, %s, %s, %s)"
        cur.execute(query, (item['id'], item['generic'], item['brand'], item['indications'], item['doctorId']))



        conn.commit()
        cur.close()
        conn.close()



    @jwt_required()
    def get(self, doctorId):
        item = self.find_by_doctorId(doctorId)
        if item:
            return item
        return []

    @classmethod
    def find_by_doctorId(cls, doctorId):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "SELECT * FROM Drug WHERE doctorId=%s"
        print(query)
        #cur.execute(query)
        cur.execute(query, (doctorId,))

        #import pdb; pdb.set_trace()
        drugs = []
        for row in cur:
            drugs.append({'id': row[0], 'generic': row[1], 'brand': row[2], 'indications': row[3], 'doctorId': row[4] })

            # connection.close()
        cur.close()
        conn.close()
        print(drugs)

        return drugs
