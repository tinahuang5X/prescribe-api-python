import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, firstName text, lastName text, username text, password text)"
cursor.execute(create_table)

# create_table = "CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)"
# cursor.execute(create_table)
#
# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")
# cursor.execute("INSERT INTO items VALUES ('test2', 12.99)")

create_table = "CREATE TABLE IF NOT EXISTS items (id INT PRIMARY KEY, doctorId INT, generic text, brand text, indications text)"
cursor.execute(create_table)
cursor.execute("INSERT INTO items VALUES (1, 1, 'atorvastatin', 'Liptor', 'lower cholesterol')")
cursor.execute("INSERT INTO items VALUES (2, 1, 'levothyroxine', 'Synthroid', 'treat hypothyroidism')")
cursor.execute("INSERT INTO items VALUES (3, 1, 'metformin', 'Glucophage', 'treat type 2 diabetes')")
cursor.execute("INSERT INTO items VALUES (4, 1, 'omeprazole', 'Prilosec', 'treat gastroesophageal reflux disease')")
cursor.execute("INSERT INTO items VALUES (5, 1, 'azithromycin', 'Zithromax', 'treat infections caused by bacteria')")



connection.commit()

connection.close()
