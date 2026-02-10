from flask import Flask,jsonify, request

import psycopg2
import os

database_name = os.environ.get("DATABASE_NAME")
user_name = os.environ.get("USER")
password = os.environ.get('PASSWORD')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')
local_host = os.environ.get("HOST")

conn = psycopg2.connect(f"user={user_name} dbname={database_name}  host={app_host} port={app_port} password={password} ")
cursor = conn.cursor()

def add_category():
  post_data = request.form if request.form else request.get_json()

  category_name = post_data.get('category_name')

  if not category_name:
    return jsonify({"message": "category_name is required"}), 400
  
  result = cursor.execute("""
    SELECT * FROM Categories
    WHERE category_name = %s
  """,(category_name,))

  result = cursor.fetchone()

  if result:
    return jsonify({"message": 'Category already exists'}), 400
  
  cursor.execute("""
    INSERT INTO Categories
      (category_name)
      VALUES(%s)
  """, (category_name,))  
  
  conn.commit()
  return jsonify({"message": f"Category {category_name} added to Database"}), 201

def get_all_categories():
  result = cursor.execute("""
    SELECT * FROM Categories;
  """)

  result = cursor.fetchall()

  record_list = []

  for record in result:
    record = {
      'category_id': record[0],
      'category_name' : record[1]
    }

    record_list.append(record)

  return jsonify({"message": "categories found", "results" : record_list}), 200 


def get_category_by_id(category_id):
  result = cursor.execute("""
    SELECT * FROM Categories
    WHERE category_id = %s
  """,(category_id,))
  result = cursor.fetchone()

  if result:
    return jsonify({"message": "Category found", "results": result}), 200
  else:
    return jsonify({"message": "Category not found"}), 404
  


def update_category(category_id):
  put_data = request.form if request.form else request.get_json()
  category_name = put_data.get("category_name")

  result = cursor.execute("""
    SELECT * FROM Categories
    WHERE category_id = %s
  """,(category_id,))

  result = cursor.fetchone()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find Category"}), 404
  
  if not category_name:
    return jsonify({"message": "category_name is required"}), 400
  
  result = cursor.execute("""
    SELECT * FROM Categories
    WHERE category_name = %s
  """,(category_name,))

  result = cursor.fetchone()

  if result:
    return jsonify({"message": 'Category already exists'}), 400
  


  result = cursor.execute("""
    UPDATE Categories 
    SET category_name = %s
    WHERE category_id = %s
  """, (category_name, category_id))
  conn.commit()
  
  return jsonify({"message": "Category updated", "results": category_name}), 200


def delete_category(category_id):
  result = cursor.execute("""
    SELECT * FROM Categories
    WHERE category_id = %s
    """,(category_id,))

  result = cursor.fetchone()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find Category"}), 404
  
    # DELETE FROM ProductsCategoriesXref
    # WHERE category_id = %s;
  result = cursor.execute("""
    DELETE FROM Categories
    WHERE category_id = %s;
  """, (category_id, category_id))
  conn.commit()

  return jsonify({"message": "Category deleted"}), 200


