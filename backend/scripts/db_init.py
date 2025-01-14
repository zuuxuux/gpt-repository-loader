# noovox/db_init.py
import os
import mysql.connector

with open("noovox/db_schema.sql", "r") as f:
    schema_sql = f.read()

conn = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST', 'localhost'),
    user=os.environ.get('MYSQL_USER', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'password'),
)

cursor = conn.cursor()
# We create the DB if not exists, then use it
for statement in schema_sql.split(';'):
    statement = statement.strip()
    if statement:
        cursor.execute(statement)
cursor.close()
conn.close()
