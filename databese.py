import psycopg2

conn = psycopg2.connect(
    dbname="faceid",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
print("✅ Database connected successfully!")
