import psycopg2


conn = psycopg2.connect(host="localhost",database="backend_dev", user="backend_admin", password="postgres")
print ("Opened database successfully")

cur = conn.cursor()

cur.execute("INSERT INTO Doctor (id, firstName, lastName, email, hashedPassword) \
      VALUES (1, 'Tina', 'Huang', 'tinahuang@gmail.com', '$2a$12$C9AYYmcLVGYlGoO4vSZTPud9ArJwbGRsJ6TUsNULzR48z8fOnTXbS' )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId) \
      VALUES (1, 'atorvastatin', 'Liptor', 'lower cholesterol', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId) \
      VALUES (2, 'levothyroxine', 'Synthroid', 'treat hypothyroidism', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId)\
      VALUES (3, 'metformin', 'Glucophage', 'treat type 2 diabetes', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId)\
      VALUES (4, 'omeprazole', 'Prilosec', 'treat gastroesophageal reflux disease ', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId)\
      VALUES (5, 'azithromycin', 'Zithromax', 'treat infections caused by bacteria', 1 )");

conn.commit()
print ("Records created successfully");
conn.close()
