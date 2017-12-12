import psycopg2
from config import config


def insert_drug(generic, brand, indications, doctorId):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO Drug(generic, brand, indications)
             VALUES(%s, %s, %s, %s) RETURNING doctorId;"""
    conn = None
    id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (generic, brand, indications, doctorId,))
        # get the generated id back
        doctorId = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return id

def insert_drugList(drugList):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO Drug(generic, brand, indications, doctorId) VALUES(%s, %s, %s, %s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,(drugList))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # insert one vendor
    insert_drug('atorvastatin',
      'Liptor',
      'lower cholesterol', doctorId)
    # insert multiple vendors

    insert_drugList([

          ('levothyroxine',
          'Synthroid',
          'treat hypothyroidism'),

        ('metformin',
          'Glucophage',
          'treat type 2 diabetes'),

        ('omeprazole',
          'Prilosec',
          'treat gastroesophageal reflux disease'),

        ('azithromycin',
          'Zithromax',
          'treat infections caused by bacteria')
      ])
