from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('generic', type=str, required=True,
    help="This field cannot be left blank!")
    parser.add_argument('brand', type=str, required=True,
    help="This field cannot be left blank!")
    parser.add_argument('indications', type=str, required=True,
    help="This field cannot be left blank!")

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
        cursor.execute(query, (item['id'], item['doctorId'], item['generic'], item['brand'], item['indications']))

        connection.commit()
        connection.close()

    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:

                return {"message": "An error occurred updating the item."}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'id': row[0], 'doctorId': row[1], 'generic': row[2], 'brand': row[3], 'indications': row[4]})

        connection.close()

        return {'items': items}
