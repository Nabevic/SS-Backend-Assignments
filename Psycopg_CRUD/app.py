from flask import Flask, jsonify, request

import psycopg2
import os

database_name = os.environ.get("DATABASE_NAME")
user_name = os.environ.get("USER")
password = os.environ.get('PASSWORD')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f"dbname={database_name} user={user_name} host={app_host} port={app_port} password={password}")
cursor = conn.cursor()

def create_all():
    print("Creating Tables...")
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS Companies (
      company_id SERIAL PRIMARY KEY,
      company_name VARCHAR UNIQUE NOT NULL,
      );
      """)
    conn.commit()
# def create_schema(cursor):

#   with open('create_table.txt','r') as readfile:
#     create_queries = readfile.read()

#   cursor.executescript(create_queries)

# result = create_schema(cursor)

app = Flask(__name__)

if __name__ == '__main__':
  create_all()
  app.run(host=app_host, port=app_port)