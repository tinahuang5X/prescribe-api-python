from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
import psycopg2
from config import config

class Patient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('name', type=str)
    parser.add_argument('dob', type=str)
    parser.add_argument('phone', type=str)
    parser.add_argument('address', type=str)
    parser.add_argument('doctorId', type=int)

    # @jwt_required()
    def get(self, doctorId):
        patient = self.find_by_doctorId(doctorId)
        if patient:
            return patient
        return {'message': 'Patient not found'}, 404

    @classmethod
    def find_by_doctorId(cls, doctorId):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "SELECT * FROM Patient WHERE doctorId=%s"
        cur.execute(query, (doctorId,))
        patient = cur.fetchone()
        conn.close()

        if patient:
            print(patient)
            return {'patient': {'id': patient[0], 'name': patient[1], 'dob': patient[2], 'phone': patient[3], 'address': patient[4], 'doctorId': patient[5] }}




class PatientOther(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('name', type=str)
    parser.add_argument('dob', type=str)
    parser.add_argument('phone', type=str)
    parser.add_argument('address', type=str)
    parser.add_argument('doctorId', type=int)
    # @jwt_required()
    @classmethod
    def find_by_id(cls, id):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "SELECT * FROM Patient WHERE id=%s"
        cur.execute(query, (id,))
        patient = cur.fetchone()
        conn.close()

        if patient:
            print('1st', patient)
            return {'patient': {'id': patient[0], 'name': patient[1], 'dob': patient[2], 'phone': patient[3], 'address': patient[4], 'doctorId': patient[5]}}

    def patch(self, id):
        data = PatientOther.parser.parse_args()
        print("100", data)
        patient = self.find_by_id(id)
        print('2nd', patient)
        updated_patient = {'id': id, 'name': data['name'], 'dob': data['dob'], 'phone': data['phone'], 'address': data['address'], 'doctorId': data['doctorId']}
        print('3rd', updated_patient)
        try:
            self.update(updated_patient)

        except:

            return {"message": "An error occurred updating the patient."}, 500
        return updated_patient


    @classmethod
    def update(cls,patient):
        data = Patient.parser.parse_args()
        conn = None

        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        if data['name']:
            query = "UPDATE Patient SET name=%s WHERE id=%s"
            cur.execute(query, (patient['name'], patient['id']))

        if data['dob']:
            query = "UPDATE Patient SET dob=%s WHERE id=%s"
            cur.execute(query, (patient['dob'], patient['id']))

        if data['phone']:
            query = "UPDATE Patient SET phone=%s WHERE id=%s"
            cur.execute(query, (patient['phone'], patient['id']))

        if data['address']:
            query = "UPDATE Patient SET address=%s WHERE id=%s"
            cur.execute(query, (patient['address'], patient['id']))


        if data['doctorId']:
            query = "UPDATE Patient SET doctorId=%s WHERE id=%s"
            cur.execute(query, (patient['doctorId'], patient['id']))



        # query = "UPDATE patient SET name=%s, dob=%s, indications=%s, doctorId=%s WHERE id=%s"
        #
        # cur.execute(query, (patient['name'], patient['dob'], patient['indications'], patient['doctorId'], patient['id']))


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

        query = "DELETE FROM Patient WHERE id=%s"
        cur.execute(query, (id,))

        conn.commit()
        cur.close()
        conn.close()
        return {'message': 'patient deleted'}



class PatientList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    parser.add_argument('name', type=str)
    parser.add_argument('dob', type=str)
    parser.add_argument('phone', type=str)
    parser.add_argument('address', type=str)
    parser.add_argument('doctorId', type=int)

    @jwt_required()
    def post(self, doctorId):

        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "SELECT MAX(id) from Patient"
        cur.execute(query)
        maxid = cur.fetchone()[0]

        # if self.find_by_doctorId(doctorId):
            # return {'message': "An patient with name '{}' already exists.".format(name)}, 400
        data = PatientList.parser.parse_args()
        print("hi", data)

        created_patient = {'id': maxid+1, 'doctorId': doctorId, 'name': data['name'], 'dob': data['dob'], 'phone': data['phone'], 'address': data['address']}
        print("hello", created_patient)

        try:
            PatientList.insert(created_patient)
        # except:
        #     return {"message": "An error occurred inserting the patient."}, 500
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return created_patient, 201

    @classmethod
    def insert(cls, patient):
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        query = "INSERT INTO Patient VALUES(%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (patient['id'], patient['name'], patient['dob'], patient['phone'], patient['address'], patient['doctorId']))



        conn.commit()
        cur.close()
        conn.close()


    @jwt_required()
    def get(self, doctorId):
        patient = self.find_by_doctorId(doctorId)
        if patient:
            return patient
        return []

    @classmethod
    def find_by_doctorId(cls, doctorId):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        conn = None
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        query = "SELECT * FROM Patient WHERE doctorId=%s"
        cur.execute(query, (doctorId,))
        #import pdb; pdb.set_trace()
        patients = []
        for row in cur:
            patients.append({'id': row[0], 'name': row[1], 'dob': row[2], 'phone': row[3], 'address': row[4], 'doctorId': row[5] })

            # connection.close()
        cur.close()
        conn.close()
        print(patients)

        return patients
