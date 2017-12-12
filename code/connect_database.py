import psycopg2

# conn = psycopg2.connect(database="testdb", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")

conn = psycopg2.connect(host="localhost",database="backend_dev", user="backend_admin", password="postgres")
print ("Opened database successfully")
