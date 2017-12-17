import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE Doctor (
            id SERIAL PRIMARY KEY,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password VARCHAR (60) NOT NULL
        )
        """,
        """
        CREATE TABLE Drug (
            id SERIAL PRIMARY KEY,
            generic TEXT,
            brand TEXT,
            indications TEXT,
            doctorId INTEGER NOT NULL REFERENCES Doctor (id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE Patient (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            doctorId INTEGER NOT NULL REFERENCES Doctor (id) ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
