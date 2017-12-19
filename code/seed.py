import psycopg2


conn = psycopg2.connect(host="localhost",database="backend_dev", user="backend_admin", password="postgres")
print ("Opened database successfully")

cur = conn.cursor()

# cur.execute("INSERT INTO Doctor (id, firstName, lastName, username, password) \
#       VALUES (1, 'Tina', 'Huang', 'tinahuang@gmail.com', 'youreawizard' )");

cur.execute("INSERT INTO Drug ( generic, brand, indications, doctorId) \
      VALUES ( 'atorvastatin', 'Liptor', 'lower cholesterol', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId) \
      VALUES ( 'levothyroxine', 'Synthroid', 'treat hypothyroidism', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId)\
      VALUES ( 'metformin', 'Glucophage', 'treat type 2 diabetes', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId)\
      VALUES ( 'omeprazole', 'Prilosec', 'treat gastroesophageal reflux disease ', 1 )");

cur.execute("INSERT INTO Drug (id, generic, brand, indications, doctorId)\
      VALUES ( 'azithromycin', 'Zithromax', 'treat infections caused by bacteria', 1 )");

cur.execute("INSERT INTO Patient (id, name, dob, phone, address, doctorId)\
      VALUES (1, 'Lisa Chang', '1/1/1987', '415-123-4567', '123 Main St. SF, CA 94102', 1 )");

cur.execute("INSERT INTO Patient (id, name, dob, phone, address, doctorId)\
      VALUES (2, 'Taylor Swift', '12/13/1989', '415-888-4438', '80 Heaven Rd. Miami, FL 39555', 1 )");

cur.execute("INSERT INTO Patient (id, name, dob, phone, address, doctorId)\
      VALUES (3, 'Justin Bieber', '3/1/1994', '510-333-4455', '100 Hollywood Dr. LA, CA 93103', 1 )");

cur.execute("INSERT INTO Patient (id, name, dob, phone, address, doctorId)\
      VALUES (4, 'Emma Stone', '11/6/1988', '925-222-4444', '48 La La Lane, LA, CA 93105', 1 )");

cur.execute("INSERT INTO Patient (id, name, dob, phone, address, doctorId)\
      VALUES (5, 'Chris Evans', '6/13/1981', '408-987-6543', '210 Captain Rd. San Diego, CA 93401', 1 )");

conn.commit()
print ("Records created successfully");
conn.close()
