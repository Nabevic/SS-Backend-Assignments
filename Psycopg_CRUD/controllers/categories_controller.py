from flask import jsonify, request
from db import connect_db

conn = connect_db()
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
  
  try:
    cursor.execute("""
      INSERT INTO Categories
        (category_name)
        VALUES(%s)
    """, (category_name,))  
    
    conn.commit()
  except:
    cursor.rollback()
    return jsonify({"message": "Category could not be added"}), 400
  
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


def category_by_id(category_id):
  if request.method == 'GET':
    result = cursor.execute("""
      SELECT * FROM Categories
      WHERE category_id = %s
    """,(category_id,))
    result = cursor.fetchone()

    if result:
      return jsonify({"message": "Category found", "results": result}), 200
    else:
      return jsonify({"message": "Category not found"}), 404
  
  elif request.method == 'PUT':
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
  
    try:
      result = cursor.execute("""
        UPDATE Categories 
        SET category_name = %s
        WHERE category_id = %s
      """, (category_name, category_id))
      conn.commit()
    except:
      cursor.rollback()
      return jsonify({"message": "Category could not be updated"}), 400
    
    return jsonify({"message": "Category updated", "results": category_name}), 200


def delete_category(category_id):
  result = cursor.execute("""
    SELECT * FROM Categories c
    LEFT JOIN ProductsCategoriesXref pcx
    ON c.category_id = pcx.category_id
    WHERE c.category_id = %s
  """,(category_id,))

  result = cursor.fetchall()

  
  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find Category"}), 404
  
  deleted_records = result
  
  try:
    result = cursor.execute("""
      DELETE FROM ProductsCategoriesXref
      WHERE category_id = %s;
                            
      DELETE FROM Categories
      WHERE category_id = %s;
    """, (category_id, category_id))
    conn.commit()
  except:
      cursor.rollback()
      return jsonify({"message": "Category could not be deleted"}), 400

  return jsonify({"message": "Category and associations deleted","result": deleted_records}), 200


