from flask import Flask, jsonify, request
from db import connect_db
import routes


conn = connect_db()
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
app.register_blueprint(routes.company)
app.register_blueprint(routes.product)
app.register_blueprint(routes.warranty)

if __name__ == '__main__':
  create_categories()
  app.run()