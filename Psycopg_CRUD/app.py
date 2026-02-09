from flask import Flask, jsonify, request

import psycopg2
import os
import routes

database_name = os.environ.get("DATABASE_NAME")
user_name = os.environ.get("USER")
password = os.environ.get('PASSWORD')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')
local_host = os.environ.get("HOST")

conn = psycopg2.connect(f"user={user_name} dbname={database_name}  host={app_host} port={app_port} password={password} ")
cursor = conn.cursor()

    # cursor.execute("""
    #   CREATE TABLE IF NOT EXISTS Companies (
    #   company_id SERIAL PRIMARY KEY,
    #   company_name VARCHAR UNIQUE NOT NULL,
    #   );
    #   """)
def create_categories():
    print("Creating Table Categories...")
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS Categories (
      category_id SERIAL PRIMARY KEY,
      category_name VARCHAR UNIQUE NOT NULL
      );
      """)
    conn.commit()
# def create_schema(cursor):

#   with open('create_table.txt','r') as readfile:
#     create_queries = readfile.read()

#   cursor.executescript(create_queries)

# result = create_schema(cursor)

app = Flask(__name__)
app.register_blueprint(routes.category)

if __name__ == '__main__':
  create_categories()
  app.run()